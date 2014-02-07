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

import tornado.ioloop
from tornadows import soaphandler, webservices, complextypes
from tornadows.soaphandler import webservice
import datetime

""" This example uses python datetime module and xml complex datatypes.
	This example simulates a service of register of users in a system
 
	python datetime.date is equivalent to xml type: xsd:date
	python datetime.datetime is equivalent to xml type: xsd:dateTime
	python datetime.time is equivalent to xml type: xsd:time
"""
class RegisterRequest(complextypes.ComplexType):
	iduser = str
	names  = str
	birthdate = datetime.date
	email  = str

class RegisterResponse(complextypes.ComplexType):
	idregister = int
	names = str
	datetimeregister = datetime.datetime
	isvalid = bool
	message = str

class RegisterService(soaphandler.SoapHandler):
	@webservice(_params=RegisterRequest, _returns=RegisterResponse)
	def register(self, register):
		iduser    = register.iduser
		names     = register.names
		birthdate = register.birthdate
		email     = register.email

		# Here you can insert the user in a database
		response = RegisterResponse()
		response.idregister = 1
		response.names      = names
		response.datetimeregister = datetime.datetime.now()
		response.isvalid = True
		response.message = 'Your register for email : %s'%email

		return response

if __name__ == '__main__':
	service = [('RegisterService',RegisterService)]
	app = webservices.WebService(service)
	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
