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

""" ToDO:
	Include all types defined for xml specification
"""

class PrimitiveType:
	pass

def createElementXML(name,type,prefix='xsd'):
	return b'<%s:element name="%s" type="%s:%s"/>'%(prefix,name,prefix,type)

def createArrayXML(name,type,prefix='xsd',maxoccurs=None):
	complexType  = b'<%s:complexType name="%sParams">\n'%(prefix,name)
	complexType += b'<%s:sequence>\n'%prefix
	if maxoccurs == None:
		complexType += b'<%s:element name="value" type="%s:%s" maxOccurs="unbounded"/>\n'%(prefix,prefix,type)
	else:
		complexType += b'<%s:element name="value" type="%s:%s" maxOccurs="%d"/>\n'%(prefix,prefix,type,maxoccurs)
	complexType += b'</%s:sequence>\n'%prefix
	complexType += b'</%s:complexType>\n'%prefix
	complexType += b'<%s:element name="%s" type="tns:%sParams"/>\n'%(prefix,name,name)
	return complexType

class Array:
	def __init__(self,type,n=None):
		self._type = type
		self._n    = n
	def createArray(self,name):
		type = self._type.getType(self._type)
		return createArrayXML(name,type,'xsd',self._n)
	def createType(self,name):
		prefix = 'xsd'
		type = self._type.getType(self._type)
		maxoccurs = self._n
		complexType = b''
		if self._n == None:
			complexType += b'<%s:element name="%s" type="%s:%s" maxOccurs="unbounded"/>\n'%(prefix,name,prefix,type)
		else:
			complexType += b'<%s:element name="%s" type="%s:%s" maxOccurs="%d"/>\n'%(prefix,name,prefix,type,maxoccurs)
		return complexType
	def genType(self,v):
		return self._type.genType(self._type,v)

class Integer(PrimitiveType):
	@staticmethod
	def createElement(name,prefix='xsd'):
		return createElementXML(name,'integer')
	@staticmethod
	def getType(self):
		return 'integer'
	@staticmethod
	def genType(self,v):
		return int(v)

class Double(PrimitiveType):
	@staticmethod
	def createElement(name,prefix='xsd'):
		return createElementXML(name,'double')
	@staticmethod
	def getType(self):
		return 'double'
	@staticmethod
	def genType(self,v):
		return float(v)

class Date(PrimitiveType):
	@staticmethod
	def createElement(name,prefix='xsd'):
		return createElementXML(name,'date')
	@staticmethod
	def getType(self):
		return 'date'
	@staticmethod
	def genType(self,v):
		return str(v)

class DateTime(PrimitiveType):
	@staticmethod
	def createElement(name,prefix='xsd'):
		return createElementXML(name,'datetime')
	@staticmethod
	def getType(self):
		return 'datetime'
	@staticmethod
	def genType(self,v):
		return str(v)

class String(PrimitiveType):
	@staticmethod
	def createElement(name,prefix='xsd'):
		return createElementXML(name,'string')
	@staticmethod
	def getType(self):
		return 'string'
	@staticmethod
	def genType(self,v):
		return str(v)
