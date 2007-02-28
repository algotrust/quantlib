
"""
 Copyright (C) 2005, 2006, 2007 Eric Ehlers
 Copyright (C) 2005 Plamen Neykov
 Copyright (C) 2005 Aurelien Chanudet

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it under the
 terms of the QuantLib license.  You should have received a copy of the
 license along with this program; if not, please email quantlib-dev@lists.sf.net
 The license is also available online at http://quantlib.org/html/license.html

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

"""generate source code for Guile addin."""

from gensrc.Addins import addin
from gensrc.Functions import function
from gensrc.Utilities import outputfile
from gensrc.Utilities import common
from gensrc.Utilities import log
from gensrc.Categories import category

class AddinGuile(addin.Addin):
    """Generate source code for Guile addin."""

    BUF_HEADER = '''SCM %s(SCM x)%s\n'''

    def generate(self, categoryList, enumerationList):
        """Generate source code for Guile addin."""

        self.categoryList_ = categoryList
        self.enumerationList_ = enumerationList

        log.Log.instance().logMessage(' begin generating Guile ...')
        self.generateInitFunc()
        self.generateFunctions()
        log.Log.instance().logMessage(' done generating Guile.')

    def generateRegistrations(self, cat):
        """Generate code to register function."""
        ret = '    /* ' + cat.displayName + ' */\n'
        stub = '    gh_new_procedure("%s", %s, 1, 0, 0);\n'
        for func in cat.getFunctions(self.name): 
            ret += stub % (func.name, func.name)
        return ret

    def generateInitFunc(self):
        """Generate initialisation function."""
        headers = ''
        registrations = ''
        i = 0
        for cat in self.categoryList_.categories(self.name):
            i += 1
            headers += '#include <' + cat.name + '.h>\n'
            registrations += self.generateRegistrations(cat)
            if i < len(self.categoryList_.categoryNames()):
                registrations += '\n'
        buf = self.bufferInitFunc.text % (headers, registrations)
        fileName = self.rootDirectory + 'qladdin.c'
        outputfile.OutputFile(self, fileName, self.copyright, buf, False)

    def generateFuncHeaders(self, cat):
        """Generate source for function prototypes."""
        prototypes = ''
        for func in cat.getFunctions(self.name): 
            prototypes += AddinGuile.BUF_HEADER % (func.name, ';\n')
        buf = self.bufferHeader.text % {
            'categoryName' : cat.name,
            'prototypes' : prototypes }
        fileName =  self.rootDirectory + cat.name + '.h'
        outputfile.OutputFile(self, fileName, cat.copyright, buf, False)

    def generateFunction(self, func):
        """Generate source code for body of function."""
        return self.bufferFunction.text % {
            'cppConversions' : func.ParameterList.generate(self.cppConversions),
            'libraryConversions' : func.ParameterList.generate(self.libraryConversions),
            'referenceConversions' : func.ParameterList.generate(self.referenceConversions),
            'enumConversions' : func.ParameterList.generate(self.enumConversions),
            'body' : func.generateBody(self),
            'returnConversion' : self.returnConversion.apply(func.returnValue),
            'name' : func.name }

    def generateFunctions(self):
        """Generate source for function implementations."""
        for cat in self.categoryList_.categories(self.name):
            self.generateFuncHeaders(cat)
            code = ''
            for func in cat.getFunctions(self.name): 
                code += AddinGuile.BUF_HEADER % (func.name, ' {')
                code += self.generateFunction(func)
            buf = self.bufferIncludes.text % {
                'includes' : cat.includeList(),
                'categoryName' : cat.name,
                'code' : code }
            fileName= self.rootDirectory + cat.name + '.cpp'
            outputfile.OutputFile(self, fileName, cat.copyright, buf, False)

