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

import tornado.httpserver
import tornado.ioloop
from tornadows import soaphandler
from tornadows import webservices
from tornadows import xmltypes
from tornadows.soaphandler import webservice

class EchoService(soaphandler.SoapHandler):
	""" Echo Service """
	@webservice(_params=xmltypes.String,_returns=xmltypes.String)
	def echo(self, message):
		return 'Echo say : %s' % message

class EchoTargetnsService(soaphandler.SoapHandler):
	""" Service to test the use of an overrided target namespace address """
	targetns_address = '192.168.0.103'
	@webservice(_params=xmltypes.String, _returns=xmltypes.String)
	def echo(self, message):
		return 'Echo say : %s' % message

class CountService(soaphandler.SoapHandler):
	""" Service that counts the number of items in a list """
	@webservice(_params=xmltypes.Array(xmltypes.String),_returns=xmltypes.Integer)
	def count(self, list_of_values):
		length = len(list_of_values)
		return length

class DivService(soaphandler.SoapHandler):
	""" Service that provides the division operation of two float numbers """
	@webservice(_params=[xmltypes.Float,xmltypes.Float],_returns=xmltypes.Float)
	def div(self, a, b):
		result = a/b
		return result

class FibonacciService(soaphandler.SoapHandler):
	""" Service that provides Fibonacci numbers """
	@webservice(_params=xmltypes.Integer,_returns=xmltypes.Array(xmltypes.Integer))
	def fib(self,n):
		a, b = 0, 1
		result = []
		while b < n:
			result.append(b)
			a, b = b, a + b
		return result

if __name__ == '__main__':
     service = [('EchoService',EchoService),
                ('EchoTargetnsService', EchoTargetnsService),
                ('CountService',CountService),
                ('DivService',DivService),
                ('FibonacciService',FibonacciService)]
     app = webservices.WebService(service)
     ws  = tornado.httpserver.HTTPServer(app)
     ws.listen(8080)
     tornado.ioloop.IOLoop.instance().start()
