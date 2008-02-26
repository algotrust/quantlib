
"""
 Copyright (C) 2007, 2008 Eric Ehlers

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <http://quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

import re
from gensrc.Types import exceptions

class FullType(object):
    """A class to merge the properties of DataType and SuperType.

    Where the same property is implemented in both DataType and SuperType,
    the value in the SuperType object is taken as a default and the
    corresponding value (if defined) in the DataType object as an override."""

    #############################################
    # class variables
    #############################################

    namespace_ = None
    classname_ = None
    RE_NAMESPACE = re.compile('(.*)::(.*)')

    #############################################
    # public interface
    #############################################

    def value(self):
        return self.value_

    def nativeType(self):
        return self.nativeType_

    def superType(self):
        return self.superType_

    def conversionSuffix(self):
        return self.conversionSuffix_

    def memberAccess(self):
        return self.memberAccess_

    def namespace(self):
        return self.namespace_

    def classname(self):
        return self.classname_

    def objectReference(self):
        return self.objectReference_

    def __init__(self, dataType, superType):

        self.value_ = dataType.value()
        if dataType.nativeType():
            self.nativeType_ = dataType.nativeType()
        elif superType.nativeType():
            self.nativeType_ = superType.nativeType()
        else:
            raise exceptions.InvalidNativeTypeException(dataType.name(), superType.name())

        self.superType_ = superType.name()
        self.conversionSuffix_ = superType.conversionSuffix()
        self.memberAccess_ = superType.memberAccess()
        self.objectReference_ = superType.objectReference()

        m = FullType.RE_NAMESPACE.match(self.value_)
        if m:
            self.namespace_ = m.group(1)
            self.classname_ = m.group(2)
