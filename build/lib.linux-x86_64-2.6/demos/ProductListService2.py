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
from tornadows import complextypes
from tornadows.soaphandler import webservice

""" This web service implements two python classes as two xml complextypes.

    THIS IS AN ALTERNATIVE IMPLEMENTATION TO ProductService.py. THIS USES 
    PYTHON TYPES FOR THE ATTRIBUTES OF THE CLASS.

    Product is a class that represents Product data structure.

	id: Is a int python type. Is the product id
	name: Is a str python type. Is the name of product. 
	price: Is a float python type. Is the price of product.
	stock: Is a int python type. Is the stock of product.

    List is a class that represents the response of the web services.
    This is a list of Product.

	product: Is a python list with a set of product (Product class).

	The operation have not input parameters.

"""

class Product(complextypes.ComplexType):
	id    = int
	name  = str
	price = float
	stock = int

class List(complextypes.ComplexType):
	product = [Product]

class ProductListService2(soaphandler.SoapHandler):
	@webservice(_params=None,_returns=List)
	def getProductList(self):

		listOfProduct = List()
		
		for i in [1,2,3,4,5,6,7]:
			reg = self.database(i)
			output = Product()
			output.id    = i
			output.name  = reg[0]
			output.price = reg[1]
			output.stock = reg[2]
	
			listOfProduct.product.append(output)

		return listOfProduct

	def database(self,id):
		""" This method simulates a database of products """
		db = {1:('COMPUTER',1000.5,100),
 		      2:('MOUSE',10.0,300),
		      3:('PENCIL BLUE',0.50,500),
		      4:('PENCIL RED',0.50,600),
		      5:('PENCIL WHITE',0.50,900),
		      6:('HEADPHONES',15.7,500),
		      7:('MACBOOK',80.78,300),
		     }
		row = (None,0.0,0)
		try:
			row = db[id]
		except:
			None
		return row
	
if __name__ == '__main__':
	service = [('ProductListService2',ProductListService2)]
	app = webservices.WebService(service)
	ws  = tornado.httpserver.HTTPServer(app)
	ws.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
