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
from tornadows import soaphandler
from tornadows import webservices
from tornadows import xmltypes
from tornadows import complextypes
from tornadows.soaphandler import webservice

import datetime

# This dictionary emulate a documental repository
repo = {}

class Document(complextypes.ComplexType):
	number = int 
	theme = str
	author = str
	text = str
	created = datetime.date

class Message(complextypes.ComplexType):
	doc = Document
	msg = str

class Repository(soaphandler.SoapHandler):
	""" Service of repository, store documents (Document)  """
	@webservice(_params=Message,_returns=str)
	def save(self, msg):
		global repo
		repo[msg.doc.number] = msg.doc
		return 'Save document number : %d'%msg.doc.number 

	@webservice(_params=int,_returns=Message)
	def find(self, num):
		global repo
		response = Message()
		try:
			doc = Document()
			d = repo[num]
			doc.number = d.number
			doc.theme = d.theme
			doc.author = d.author
			doc.text = d.text
			doc.created = d.created
			response.doc = doc
			response.msg = 'OK'
		except:
			response.doc = Document()
			response.msg = 'Document number %d dont exist'%num
		return response

if __name__ == '__main__':
  	service = [('RepositoryService',Repository)]
  	app = webservices.WebService(service).listen(8080)
  	tornado.ioloop.IOLoop.instance().start()
