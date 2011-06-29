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

""" Class Wsdl to generate WSDL Document """
import xml.dom.minidom
from tornadows import xmltypes

class Wsdl:
	""" ToDO:
		- Incorporate exceptions for parameters inputs.
		- When elementInput and/or elementOutput are empty trigger a exception.
	"""
	def __init__(self,nameservice=None,targetNamespace=None,arguments=None,elementInput=(),elementOutput=(),operation=None,location=None):
		self._nameservice = nameservice
		self._namespace = targetNamespace
		self._arguments = arguments
		self._elementNameInput = elementInput[0]
		self._elementInput = elementInput[1]
		self._elementNameOutput = elementOutput[0]
		self._elementOutput = elementOutput[1]
		self._operation = operation
		self._location = location

	def createWsdl(self):
		typeInput  = None
		typeOutput = None
		types  = b'<wsdl:types>\n'
		types += b'<xsd:schema targetNamespace="%s">\n'%self._namespace
		if isinstance(self._elementInput,dict):
			typeInput = self._elementNameInput
			types += self._createComplexTypes(self._elementNameInput, self._arguments, self._elementInput)
		elif isinstance(self._elementInput,xmltypes.Array):
			typeInput  = self._elementNameInput
			types += self._elementInput.createArray(typeInput)
		elif isinstance(self._elementInput,list) or issubclass(self._elementInput,xmltypes.PrimitiveType):
			typeInput  = self._elementNameInput
			types += self._createTypes(typeInput,self._elementInput)
		if isinstance(self._elementOutput,xmltypes.Array):
			typeOutput = self._elementNameOutput
			types += self._elementOutput.createArray(typeOutput)
		elif isinstance(self._elementOutput,list) or issubclass(self._elementOutput,xmltypes.PrimitiveType):
			typeOutput = self._elementNameOutput
			types += self._createTypes(typeOutput,self._elementOutput)
		types += b'</xsd:schema>\n'
		types += b'</wsdl:types>\n'
		messages  = b'<wsdl:message name="%sRequest">\n'%self._nameservice
		messages += b'<wsdl:part name="parameters" element="tns:%s"/>\n'%typeInput
		messages += b'</wsdl:message>\n'
		messages += b'<wsdl:message name="%sResponse">\n'%self._nameservice
		messages += b'<wsdl:part name="parameters" element="tns:%s"/>\n'%typeOutput
		messages += b'</wsdl:message>\n'
		portType  = b'<wsdl:portType name="%sPortType">\n'%self._nameservice
		portType += b'<wsdl:operation name="%s">\n'%self._operation
		portType += b'<wsdl:input message="tns:%sRequest"/>\n'%self._nameservice
		portType += b'<wsdl:output message="tns:%sResponse"/>\n'%self._nameservice
		portType += b'</wsdl:operation>\n'
		portType += b'</wsdl:portType>\n'
		binding  = b'<wsdl:binding name="%sBinding" type="tns:%sPortType">\n'%(self._nameservice,self._nameservice)
		binding += b'<soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>\n'
		binding += b'<wsdl:operation name="%s">\n'%self._operation
		binding += b'<soap:operation soapAction="%s" style="document"/>\n'%self._location
		binding += b'<wsdl:input><soap:body use="literal"/></wsdl:input>\n'
		binding += b'<wsdl:output><soap:body use="literal"/></wsdl:output>\n'
		binding += b'</wsdl:operation>\n'
		binding += b'</wsdl:binding>\n'
		service  = b'<wsdl:service name="%s">\n'%self._nameservice
		service += b'<wsdl:port name="%sPort" binding="tns:%sBinding">\n'%(self._nameservice,self._nameservice)
		service += b'<soap:address location="%s"/>\n'%self._location
		service += b'</wsdl:port>\n'
		service += b'</wsdl:service>\n'

		definitions  = b'<wsdl:definitions name="%s"\n'%self._nameservice
		definitions  += b'xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n'
		definitions  += b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
		definitions  += b'xmlns:tns="%s"\n'%self._namespace
		definitions  += b'xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"\n'
		definitions  += b'xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"\n'
		definitions  += b'targetNamespace="%s">\n'%self._namespace
		definitions += types
		definitions += messages
		definitions += portType
		definitions += binding
		definitions += service
		definitions += b'</wsdl:definitions>\n'
		wsdlXml = xml.dom.minidom.parseString(definitions)

		return wsdlXml

	def _createTypes(self, name, elements):
		elem = b''
		if isinstance(elements,list):
			elem = b'<xsd:complexType name="%sParams">\n'%name
			elem += b'<xsd:sequence>\n'
			elems = b''
			idx = 1
			for e in elements:
				elems += e.createElement('value%s'%idx)+'\n'
				idx += 1
			elem += elems+b'</xsd:sequence>\n'
			elem += b'</xsd:complexType>\n'
			elem += b'<xsd:element name="%s" type="tns:%sParams"/>\n'%(name,name)
		elif issubclass(elements,xmltypes.PrimitiveType):
			elem = elements.createElement(name)+'\n'

		return elem

	def _createComplexTypes(self, name, arguments, elements):
		elem = b''
		if isinstance(elements,dict):
			elem = b'<xsd:complexType name="%sTypes">\n'%name
			elem += b'<xsd:sequence>\n'
			elems = b''
			for e in arguments:
				if  isinstance(elements[e],xmltypes.Array):
					elems += elements[e].createType(e)
				elif issubclass(elements[e],xmltypes.PrimitiveType):
					elems += elements[e].createElement(e)+'\n'
			elem += elems+b'</xsd:sequence>\n'
			elem += b'</xsd:complexType>\n'
			elem += b'<xsd:element name="%s" type="tns:%sTypes"/>\n'%(name,name)
		elif issubclass(elements,xmltypes.PrimitiveType):
			elem = elements.createElement(name)+'\n'

		return elem
