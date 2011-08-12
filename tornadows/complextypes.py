#!/usr/bin/env python
#
# Copyright 2011 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations

""" Implementation of module with classes and functions for transform python 
    classes in xml schema: 

    See the next example:

    class Person:
	name = StringProperty()
	age  = IntegerProperty()

    is equivalent to:

     <xsd:complexType name="Person">
	<xsd:sequence>
		<xsd:element name="name" type="xsd:string"/>
		<xsd:element name="age" type="xsd:integer"/> 
	</xsd:sequence>
     </xsd:complexType>
"""

import tornadows.xmltypes

class Property:
	""" Class base for definition of properties of the attributes of a python class """
	type  = None
	value = None

class IntegerProperty(Property):
	""" Class for definitions of Integer Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Integer
		self.value = None

class DecimalProperty(Property):
	""" Class for definitions of Decimal Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Decimal
		self.value = None

class DoubleProperty(Property):
	""" Class for definitions of Double Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Double
		self.value = None

class FloatProperty(Property):
	""" Class for definitions of Float Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Float
		self.value = None

class DurationProperty(Property):
	""" Class for definitions of Duration Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Duration
		self.value = None

class DateProperty(Property):
	""" Class for definitions of Date Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Date
		self.value = None

class TimeProperty(Property):
	""" Class for definitions of Time Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Time
		self.value = None

class DateTimeProperty(Property):
	""" Class for definitions of DateTime Property """
	def __init__(self):
		self.type = tornadows.xmltypes.DateTime
		self.value = None

class StringProperty(Property):
	""" Class for definitions of String Property """
	def __init__(self):
		self.type = tornadows.xmltypes.String
		self.value = None

class BooleanProperty(Property):
	""" Class for definitions of Boolean Property """
	def __init__(self):
		self.type = tornadows.xmltypes.Boolean
		self.value = None

class ComplexType:
	""" Class for definitions of python class like xml document and schema:
	    
	    import tornadows.complextype

	    class Person(tornadows.complextype.ComplexType):
		name = tornadows.complextype.StringProperty()
		age  = tornadows.complextype.IntegerProperty()

	    if __name__ == '__main__':
		print Person.toXSD()

		p = Person()
		p.name.value = 'Steve J'
		p.age.value = 18
		print p.toXML()
		 
	"""
	def toXML(self):
		""" Method for get the xml document with the value. Return a string 
		    with the xml document.
		"""
		xml = b'<%s>\n'%self.__class__.__name__
		for key in self.__class__.__dict__.keys():
			element = self.__class__.__dict__[key]
			if isinstance(element,Property):
				xml += b'<%s>%s</%s>\n'%(key,element.value,key)
		xml += b'</%s>\n'%self.__class__.__name__
		return xml
	@classmethod
	def toXSD(cls,xmlns='http://www.w3.org/2001/XMLSchema',namespace='xsd'):
		""" Class method for get the xml schema with the document definition.
		    Return a string with the xsd document.
		 """
		name = cls.__name__
		xsd = b'<%s:complexType name="%s" xmlns:%s="%s">\n'%(namespace,name,namespace,xmlns)
		xsd += b'<%s:sequence>\n'%namespace
		for key in cls.__dict__.keys():
			element = cls.__dict__[key]
			if isinstance(element,Property):
				xsd += element.type.createElement(str(key))+'\n'
		xsd += b'</%s:sequence>\n'%namespace
		xsd += b'</%s:complexType>\n'%namespace
		return xsd
	@classmethod
	def getName(cls):
		""" Class method return the name of the class """
		return cls.__name__
