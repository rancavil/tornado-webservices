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
from tornadows import xmltypes
from tornadows import webservices
from tornadows import complextypes
from tornadows.soaphandler import webservice

""" This web services shows how uses complextypes and classes python.

	User is a python class with two attributes:
		username : is a python str type with the username.
		roles    : is a python list of str (roles for the username).

	ListOfUser is another class with two attributes:
		idlist : is a python str type.
		roles  : is a python list of User (python class).

"""
class User(complextypes.ComplexType):
	username = str
	roles = [str]

class ListOfUser(complextypes.ComplexType):
	idlist = int
	list = [User]

class UserRolesService(soaphandler.SoapHandler):
	@webservice(_params=xmltypes.Integer,_returns=ListOfUser)
	def getUsers(self, idlist):
		user1 = User()
		user1.username = 'steve'
		user1.roles = ['ceo','admin']
		
		user2 = User()
		user2.username = 'billy'
		user2.roles = ['developer']

		listusers = ListOfUser()
		listusers.idlist = idlist
		listusers.list = [user1, user2]

		return listusers
	
if __name__ == '__main__':
	service = [('UserRolesService',UserRolesService)]
	app = webservices.WebService(service)
	ws  = tornado.httpserver.HTTPServer(app)
	ws.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
