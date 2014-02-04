#!/usr/bin/env python
# -*- coding: utf8 -*-
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
from tornadows import complextypes
from tornadows.soaphandler import webservice

""" This web service implements two python classes as two xml complextypes.

    Input is a class that represents the input parameter (request) for the
    web service:

	idProduct : is a instance of IntegerProperty(). This create a subclass
		    of Property with value attribute (for store the value) and
		    type attribute for store the xmltype.

    Product is a class that represents the response of the web service.

	id: Is a instance of IntegerProperty() that store the id of product
	name: Is a instance of StringProperty() that store the name of product 
	price: Is a instance of FloatProperty() that store the price of product
	stock: Is a instance of IntegerProperty() that store the stock of product

"""

class Input(complextypes.ComplexType):
	idProduct = complextypes.IntegerProperty()

class Product(complextypes.ComplexType):
	id    = complextypes.IntegerProperty()
	name  = complextypes.StringProperty()
	price = complextypes.FloatProperty()
	stock = complextypes.IntegerProperty()

class ProductService(soaphandler.SoapHandler):
	@webservice(_params=Input,_returns=Product)
	def getProduct(self, input):
		id = input.idProduct.value
		
		reg = self.database(id)

		output = Product()

		output.id.value    = id
		output.name.value  = reg[0]
		output.price.value = reg[1]
		output.stock.value = reg[2]

		return output

	def database(self,id):
		""" This method simulates a database of products """
		db = {1:('COMPUTER',1000.5,100),
 		      2:('MOUSE',10.0,300),
		      3:('PENCIL BLUE',0.50,500),
		      4:('PENCIL RED',0.50,600),
		      5:('PENCIL WHITE',0.50,900),
		      6:('HEADPHONES',15.7,500),
		      7:(u'Japanses Noodles (ラーメン)',1.1,500),
		     }
		row = (None,0.0,0)
		try:
			row = db[id]
		except:
			None
		return row
	
if __name__ == '__main__':
	service = [('ProductService',ProductService)]
	app = webservices.WebService(service)
	ws  = tornado.httpserver.HTTPServer(app)
	ws.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
