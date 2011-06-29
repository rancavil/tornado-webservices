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
# under the License.

""" Implementation of soaphandler for webservices API 0.9 """

import tornado.httpserver
import tornado.web
import xml.dom.minidom
import string
import inspect
from tornadows import soap
from tornadows import xmltypes
from tornadows import wsdl

""" Global variable. If you want use your own wsdl file """
wsdl_path = None

def webservice(*params,**kwparams):
	""" Decorator method for web services operators """
	def method(f):
		_input = None
		_output = None
		_inputArray = False
		_outputArray = False
		if len(kwparams):
			_params = kwparams['_params']
			if isinstance(_params,list):
				_args = inspect.getargspec(f).args[1:]
				_input = {}
				i = 0
				for arg in _args:
					_input[arg] = _params[i]
					i+=1
			else:
				_args = inspect.getargspec(f).args[1:]
				_input = {}
				for arg in _args:
					_input[arg] = _params
				if isinstance(_params,xmltypes.Array):
					_inputArray = True

			_returns = kwparams['_returns']
			if isinstance(_returns,xmltypes.Array):
				_output = _returns
				_outputArray = True
			elif isinstance(_returns,list) or issubclass(_returns,xmltypes.PrimitiveType):
				_output = _returns
		def operation(*args,**kwargs):
			return f(*args,**kwargs)

		operation.func_name = f.func_name
		operation._is_operation = True
		operation._args = _args
		operation._input = _input
		operation._output = _output
		operation._operation = f.func_name
		operation._inputArray = _inputArray
		operation._outputArray = _outputArray
		return operation
	return method

def soapfault(faultstring):
	""" Method for generate a soap fault
	    soapfault() return a SoapMessage() object with a message 
	    for Soap Envelope
	 """
	fault = soap.SoapMessage()
	faultmsg  = b'<soapenv:Fault xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope">\n'
	faultmsg += b'<faultcode></faultcode>\n'
	faultmsg += b'<faultstring>%s</faultstring>\n'%faultstring
	faultmsg += b'</soapenv:Fault>\n'
	fault.setBody(xml.dom.minidom.parseString(faultmsg))
	return fault

class SoapHandler(tornado.web.RequestHandler):
	""" This subclass extends tornado.web.RequestHandler class, defining the 
	    methods get() and post() for handle a soap message (request and response).
	 """
	def get(self):
		""" Method get() returned the WSDL. If wsdl_path is null, the
		    WSDL is generated dinamically.
		"""
		address = tornado.httpserver.socket.gethostbyname(tornado.httpserver.socket.gethostname())
		port = self.request.headers['Host'].split(':')[1]
		wsdl_nameservice = self.request.uri.replace('/','').replace('?wsdl','').replace('?WSDL','')
		wsdl_input       = None
		wsdl_output      = None
		wsdl_operation   = None
		wsdl_args        = None

		for operations in dir(self):
			operation = getattr(self,operations)
			if callable(operation) and hasattr(operation,'_input') and hasattr(operation,'_output') and hasattr(operation,'_operation') \
					       and hasattr(operation,'_args'):
				wsdl_input     = getattr(operation,'_input')
				wsdl_output    = getattr(operation,'_output')
				wsdl_operation = getattr(operation,'_operation')
				wsdl_args      = getattr(operation,'_args')

		wsdl_targetns = 'http://%s:%s/%s/%s'%(address,port,wsdl_nameservice,wsdl_operation)
		wsdl_location = 'http://%s:%s/%s'%(address,port,wsdl_nameservice)
		query = self.request.query
		self.set_header('Content-Type','application/xml; charset=UTF-8')
		if string.upper(query) == 'WSDL':
			if wsdl_path == None:
				wsdlfile = wsdl.Wsdl(nameservice=wsdl_nameservice,
						     targetNamespace=wsdl_targetns,
						     arguments=wsdl_args,
						     elementInput=('params',wsdl_input),
					    	     elementOutput=('returns',wsdl_output),
					     	     operation=wsdl_operation,
					     	     location=wsdl_location)
				self.finish(wsdlfile.createWsdl().toxml())
			else:
				fd = open(str(wsdl_path),'r')
				xmlWSDL = ''
				for line in fd:
					xmlWSDL += line
				fd.close()
				self.finish(xmlWSDL)

	def post(self):
		""" Method post() to process of requests and responses SOAP messages """
		try:
			self._request = self._parseSoap(self.request.body)
			self.set_header('Content-Type','text/xml')
			for operations in dir(self):
				operation = getattr(self,operations)
				if callable(operation) and hasattr(operation,'_is_operation'):
					params = []
					response = None
					types = getattr(operation,'_input')
					params = self._parseParams(self._request.getBody()[0],params,types)
					if hasattr(operation,'_inputArray') and getattr(operation,'_inputArray'):
						response = operation(params)
					else:
						response = operation(*params)
					is_array = None
					if hasattr(operation,'_outputArray') and getattr(operation,'_outputArray'):
						is_array = getattr(operation,'_outputArray')
					self._response = self._createReturns(response,is_array)

			soapmsg = self._response.getSoap().toxml()
			self.write(soapmsg)
		except Exception as detail:
			fault = soapfault('Error in web service : %s'%detail)
			self.write(fault.getSoap().toxml())

	def _parseSoap(self,xmldoc):
		""" Private method parse a message soap from a xmldoc like string
		    _parseSoap() return a soap.SoapMessage().
		"""
		xmldoc = xmldoc.replace('\n',' ').replace('\t',' ').replace('\r',' ')
		document = xml.dom.minidom.parseString(xmldoc)
		prefix = document.documentElement.prefix
		header = None
		body = None
		if prefix != None:
			header = document.getElementsByTagName(prefix+':Header')
			body = document.getElementsByTagName(prefix+':Body')
		else:
			header = document.getElementsByTagName('Header')
			body = document.getElementsByTagName('Body')

		header_elements = self._parseXML(header)
		body_elements = self._parseXML(body)
		
		soapMsg = soap.SoapMessage()
		for h in header_elements:
			soapMsg.setHeader(h)
		for b in body_elements:
			soapMsg.setBody(b)

		return soapMsg

	def _parseXML(self,elements):
		""" Private method parse and digest the xml.dom.minidom.Element 
		    finding the childs of Header and Body from soap message. 
		    Return a list object with all of child Elements.
		"""
		elem_list = []
		if len(elements) <= 0:
			return elem_list
		if elements[0].childNodes.length <= 0:
			return elem_list
		for element in elements[0].childNodes:
			if element.nodeType == element.ELEMENT_NODE:
				prefix = element.prefix
				namespace = element.namespaceURI
				if prefix != None and namespace != None:
					element.setAttribute('xmlns:'+prefix,namespace)
				elem_list.append(xml.dom.minidom.parseString(element.toxml()))
		return elem_list
	
	def _parseParams(self,elements,params,types=None):
		""" Private method to parse a Body element of SOAP Envelope and extract
		    the values of the request document like parameters for the soapmethod,
		    this method return a list values of parameters.
		 """
		if elements.hasChildNodes:
			for element in elements.childNodes:
				if element.nodeType == element.TEXT_NODE:
					s = str(element.nodeValue)
					if s.strip() != '':
						name = element.parentNode.tagName
						v = None
						if isinstance(types[name],xmltypes.Array):
							v = types[name].genType(str(element.nodeValue.strip()))
						else:
							v = types[name].genType(types[name],str(element.nodeValue.strip()))
						params.append(v)
				else:
					self._parseParams(element,params,types)
			return params
	
	def _createReturns(self,result,is_array):
		""" Private method to generate the xml document with the response. 
		    Return a SoapMessage().
		"""
		xmlresponse = ''
		if isinstance(result,list):
			xmlresponse = '<returns>\n'
			i = 1
			for r in result:
				if is_array == True:
					xmlresponse += '<value>%s</value>\n'%str(r)
				else:
					xmlresponse += '<value%d>%s</value%d>\n'%(i,str(r),i)
				i+=1
			xmlresponse += '</returns>\n'
		else:
			xmlresponse = '<returns>%s</returns>\n'%str(result)
	
		response = xml.dom.minidom.parseString(xmlresponse)
		
		soapResponse = soap.SoapMessage()
		soapResponse.setBody(response)
		return soapResponse
