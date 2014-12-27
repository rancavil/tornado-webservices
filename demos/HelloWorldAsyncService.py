# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2014 Jonatan Alexis Anauati
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
import tornado.gen
import tornado.httpserver
import tornado.ioloop

from tornadows import soaphandler, webservices, xmltypes
from tornadows.soaphandler import webservice

class HelloWorldAsyncService(soaphandler.SoapHandler):
    """ Async service that returns 'Hello World!!!' """
    @tornado.gen.coroutine
    @webservice(_params=None,_returns=xmltypes.String)
    def sayHello(self):
        raise tornado.gen.Return('Hello World!!!')

if __name__ == '__main__':
    service = [('HelloWorldAsyncService', HelloWorldAsyncService)]
    app = webservices.WebService(service)
    ws = tornado.httpserver.HTTPServer(app)
    ws.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
