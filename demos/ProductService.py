import tornado.httpserver
import tornado.ioloop
from tornadows import soaphandler
from tornadows import webservices
from tornadows import complextypes
from tornadows.soaphandler import webservice

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
