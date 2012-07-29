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

class MathService(soaphandler.SoapHandler):
	""" Service that provides math operations of two float numbers """
	@webservice(_params=[float,float],_returns=float)
	def add(self, a, b):
		result = a+b
		return result
	@webservice(_params=[float,float],_returns=float)
	def sub(self, a, b):
		result = a-b
		return result
	@webservice(_params=[float,float],_returns=float)
	def mult(self, a, b):
		result = a*b
		return result
	@webservice(_params=[float,float],_returns=float)
	def div(self, a, b):
		result = a/b
		return result

if __name__ == '__main__':
  	service = [('MathService',MathService)]
  	app = webservices.WebService(service)
  	ws  = tornado.httpserver.HTTPServer(app)
  	ws.listen(8080)
  	tornado.ioloop.IOLoop.instance().start()
