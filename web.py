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


import http.client
import json
import http.server

class OpenFDAParser():

	def get_company(self,events):
		#conseguir companias a partir de  drogas
		company=[]
		for event in events['results']:
			company+=[event["companynumb"]]
		return company

	def get_drug(self,events):
		#conseguir drogas a partir de companias
		company=[]
		for event in events['results']:
			company+=[event["patient"]["drug"][0]["medicinalproduct"]]
		return company

	def lista_drug(self,event):
		#lista drogas
		lista=[]
		event1=event["results"]
		for event in event1:
			event2=event["patient"]["drug"][0]["medicinalproduct"]
			event3=json.dumps(event2)
			lista+=[event3]
		return lista

	def lista_company(self,event):
		#lista de companias
		lista=[]
		event1=event["results"]
		for event in event1:
			event2=event["companynumb"]
			event3=json.dumps(event2)
			lista+=[event3]
			#transforma a string
		return lista

	def lista_patient_sex(self,event):
		#lista de sexos
		lista=[]
		event1=event["results"]
		for event in event1:
			event2=event["patient"]["patientsex"]
			event3=json.dumps(event2)
			lista+=[event3]
			#transforma a string
		return lista
	
	def lista_drug_authorization(self,event):
		lista=[]
		event1=event["results"]
		for event in event1:
			if "drugauthorizationnumb" in event["patient"]["drug"][0]:
				event2=event["patient"]["drug"][0]["drugauthorizationnumb"]
			else:
				event2="-"
			event3=json.dumps(event2)
			lista+=[event3]
			#transforma a string
		return lista


class OpenFDAClient():
	OPENFDA_API_URL="api.fda.gov"
	OPENFDA_API_EVENT="/drug/event.json"
	OPEN_DRUG="/drug/event.json?search=patient.drug.medicinalproduct:"
	OPEN_COMPANY="/drug/event.json?search=companynumb:"
	def get_event(self,limite):
			conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
			#de la biblioteca coge httpsconnection que permite establecer conexiones https con una url.Crea un cliente.


			conn.request("GET",self.OPENFDA_API_EVENT + "?limit="+ limite + "&")
			#haces una peticion de tipo get y pides /. get es un metodo.get es para coger algo.conecta cliente y servidor.hace una peticion y la guarda.PETICION


			r1 = conn.getresponse()
			#consigue una respuesta y la guarda en r1.RESPUESTA.
			#r1 es como un fichero


			print(r1.status, r1.reason)
			#no relevante.comunica es estado de la peticion(si ha ido bien) y reason
			#debe imprimir 200 OK.NO IMPORTANTE.


			data1 = r1.read()
			# This will return entire content.

			data1=data1.decode("utf8")
			#transformar de bytes a string
			data2=json.loads(data1)
			return data2


	def get_event_drug(self,limit):
		#conseguir drogas para buscar companias

			conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
			conn.request("GET",self.OPEN_DRUG +limit+ "&limit=10")
			r1 = conn.getresponse()
			print(r1.status, r1.reason)
			data1 = r1.read()
			data1=data1.decode("utf8")
			data2=json.loads(data1)
			return data2

	def get_event_company(self,limit):
		#conseguir companias para buscar drogas
			conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
			conn.request("GET",self.OPEN_COMPANY +limit+ "&limit=10")
			r1 = conn.getresponse()
			print(r1.status, r1.reason)
			data1 = r1.read()
			data1=data1.decode("utf8")
			data2=json.loads(data1)
			return data2

class OpenFDAHTML():
	def html_companies(self,lista):


		html_event="""
		<html>
			<head></head>
			<body>
				<h1>Companias</h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event += """		</ol>
			</body>
		</html>
		"""
		return html_event

	def html_patient_sex(self,lista):


		html_event="""
		<html>
			<head></head>
			<body>
				<h1>Sexo de los pacientes</h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event += """		</ol>
			</body>
		</html>
		"""
		return html_event



	def get_main_page(self):
		html = """
		<html>
			<head>
				<title>Open FDA Cool App</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method="get" action="listDrugs">
					<input style="background-color: #b1fffa" type="submit" value="Drug list">
					</input>
					limit:
					  <input  style="background-color: #fff9dc" name="limit" type="text">
                    </input>
				</form>
				<form method="get" action="searchDrug">
					drug:
				   <input  style="background-color: #fff9dc" name="drug" type="text">
                    </input>
					<input style="background-color: #fbbe00" type="submit" value="Drug search ">
					</input>
				</form>
				<form method="get" action="listCompanies">
					<input style="background-color: #b1fffa" type="submit" value="Company list">
					</input>
					    limit:
				   <input style="background-color: #fff9dc" name="limit" type="text">
                    </input>
				</form>
				<form method="get" action="searchCompany">
					company:
				   <input style="background-color: #fff9dc" name="company" type="text" >
                    </input>

					<input style="background-color: #fbbe00" type="submit" value="Company search"
					</input>
				</form>
				<form method="get" action="listGender">
					<input style="background-color: #b1fffa" type="submit" value="listGender">
					</input>
					    limit:
				   <input style="background-color: #fff9dc" name="limit" type="text">
                    </input>
				</form>
			</body>
		</html>
		"""
		return html

	def get_main_page2(self):
		html = """
		<html>
			<head>
				<title>Open FDA Cool App</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method="get" action="Drugauthorization">
					<input style="background-color: #b1fffa" type="submit" value="Drug authorization">
					</input>
					limit:
					  <input  style="background-color: #fff9dc" name="limit" type="text">
                    </input>
				</form>
			</body>
		</html>
		"""
		return html

	def html_404(self):
		html = """
		<html>
			<head>
				<title>Error 404 Not found</title>
			</head>
			<body>
				<h1>Error 404 Not found </h1>
			</body>
		</html>
		"""
		return html



	def html_medicines(self,lista):
		html_event="""
		<html>
			<head></head>
			<body>
				<h1>Medicamentos</h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event += """		</ol>
			</body>
		</html>
		"""
		return html_event

	def html_drugauthorizationnumb(self,lista):
		html_event="""
		<html>
			<head></head>
			<body>
				<h1>Drug authoritation numb</h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event += """		</ol>
			</body>
		</html>
		"""
		return html_event





class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	# GET




	def get_word(self):
		#separar palabra
		drug1=self.path.split("=")[1]
		return drug1






	def do_GET(self):
		parser=OpenFDAParser()
		client=OpenFDAClient()
		html=OpenFDAHTML()
		main_page=False
		is_main_page2=False
		is_event_drug=False
		is_search_drug=False
		is_event_company=False
		is_search_company=False
		is_patient_sex=False
		is_error=False
		is_found=False
		is_secret=False
		is_redirect=False
		is_drug_authorization=False
		if self.path=="/":
			main_page=True
			is_found=True
		elif "searchDrug" in self.path:
			is_search_drug=True
			is_found=True
		elif "listDrugs" in self.path:
		   is_event_drug=True
		   is_found=True
		elif "listCompanies" in self.path:
			is_event_company=True
			is_found=True
		elif "searchCompany" in self.path:
			is_search_company=True
			is_found=True
		elif "listGender" in self.path:
			is_patient_sex=True
			is_found=True
		elif "/secret" in self.path:
			is_secret=True
			is_found=True
		elif "redirect" in self.path:
			is_redirect=True
			is_found=True
		elif "/another" in self.path:
			is_found=True
			is_main_page2=True
		elif "authorization" in self.path:
			is_found=True
			is_drug_authorization=True
		else:
			is_error=True

		if is_secret:
			self.send_response(401)
			self.send_header('WWW-Authenticate','Basic realm="Login required"')

		elif is_redirect:
			self.send_response(302)
			self.send_header("Location","/")

		elif is_found:
		# Send response status code
			self.send_response(200)
			self.send_header('Content-type','text/html')
		else:
			self.send_response(404)
			self.send_header('Content-type','text/html')
		# Send headers

		self.end_headers()
		# Send message back to client
		#message = "Hello world! " + self.path
		# Write content as utf-8 data
		html_mainpage=html.get_main_page()
		if main_page:
			self.wfile.write(bytes(html_mainpage, "utf8"))
			
		elif is_main_page2:
			html2=html.get_main_page2()
			self.wfile.write(bytes(html2, "utf8"))
		elif is_event_drug:
			limite=self.get_word()
			event=client.get_event(limite)
			lista=parser.lista_drug(event)
			html_drug=html.html_medicines(lista)
			self.wfile.write(bytes(html_drug, "utf8"))

		elif is_search_drug:
			limite=self.get_word()
			event_drug=client.get_event_drug(limite)
			search2=parser.get_company(event_drug)
			html_drugs=html.html_companies(search2)
			self.wfile.write(bytes(html_drugs, "utf8"))
			#lo meto dentro de la condicion para que se ejecute solo al dar al boton

		elif is_event_company:
			limite=self.get_word()
			event=client.get_event(limite)
			lista=parser.lista_company(event)
			html_companies=html.html_companies(lista)
			self.wfile.write(bytes(html_companies, "utf8"))

		elif is_search_company:
			limite=self.get_word()
			event_company=client.get_event_company(limite)
			search2=parser.get_drug(event_company)
			html_company=html.html_medicines(search2)
			self.wfile.write(bytes(html_company, "utf8"))

		elif is_patient_sex:
			limite=self.get_word()
			event=client.get_event(limite)
			lista=parser.lista_patient_sex(event)
			html_sex=html.html_patient_sex(lista)
			self.wfile.write(bytes(html_sex, "utf8"))

		elif is_drug_authorization:
			limite=self.get_word()
			event=client.get_event(limite)
			lista=parser.lista_drug_authorization(event)
			html_authorization=html.html_drugauthorizationnumb(lista)
			self.wfile.write(bytes(html_authorization, "utf8"))

		elif is_error:
			html_error=html.html_404()
			self.wfile.write(bytes(html_error,"utf8"))

		return

