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

""" This example uses python datetime module. 
	python datetime.date is equivalent to xml type: xsd:date
	python datetime.datetime is equivalent to xml type: xsd:dateTime
	python datetime.time is equivalent to xml type: xsd:time
"""
class InputRequest(complextypes.ComplexType):
	idperson = str

class CertificateResponse(complextypes.ComplexType):
	numcert = int
	idperson = str
	nameperson = str
	birthday = datetime.date
	datetimecert = datetime.datetime
	isvalid = bool

class CertService(soaphandler.SoapHandler):
	@webservice(_params=InputRequest, _returns=CertificateResponse)
	def getCertificate(self, input):
		idperson = input.idperson

		cert = CertificateResponse()
		cert.numcert = 1
		cert.idperson = idperson
		cert.nameperson = 'Steve J'
		cert.birthday = datetime.date(1973,12,11)
		cert.datetimecert = datetime.datetime.now()
		cert.isvalid = True

		return cert

if __name__ == '__main__':
	service = [('CertService',CertService)]
	app = webservices.WebService(service)
	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
