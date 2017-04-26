#Copyright [yyyy] [name of copyright owner]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#Author:Alberto Guzman Merino

#web server
import socketserver
import  web
PORT=8000
socketserver.TCPServer.allow_reuse_address=True
#Handler = http.server.SimpleHTTPRequestHandler
Handler=web.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
#Handler es un objeto y TCPServer una clase(por los parentesis).httpd es un objeto.Hnadler es un objeto con el que conecta el cliente.handler es un objeto dentro de httpd.Explicas al objeto como atender a los clientes y necesitras objetos handler y creas una clase Handler(BIBLIOTECA) que te lo crea."Tienes un objeto y llamas a una clase pra que te haga cosas"

print ("serving at port",PORT)
httpd.serve_forever()
#bucleinfinito


