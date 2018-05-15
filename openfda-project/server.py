import http.server
import http.client
import socketserver
import json

#Tras importar los módulos que nos seran necesarios más necesarios, definimos el puerto donde se lanzara el servidor
PORT = 8000

# Definimos la clase. Es derivada de BaseHTTPRequestHandler.  Esto es que hereda todos los métodos de esta clase.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    #Nombramos unas variables que utilizaremos mucho posteriormente para simplificar y hacer mas visible el código
    OPENFDAURL = "api.fda.gov"
    OPENFDAPATH = "/drug/label.json"
    OPENFDADRUG = "&search=active_ingredient:"
    OPENFDACOMPANY= "&search=openfda.manufacturer_name:"

    #Con una funcion creamos como va a ser nuestro servidor
    #Esto puede ser cuan largo y sofisticado como deseemos(colores, fotos, efectos...), yo lo he diseñado con inputs
    #Segun donde entre el cliente o que escriba en el buscador le imprimira la informacion correspondiente que leera de OPENFDA
    def get_server(self):
        html="""
            <html>
                <head>
                    <title>JGalant App for OpenFDA</title>
                </head>
                <body>
                    <h1>OpenFDA App</h1>

                    <body style='background-color: lightGrey'>
                    <B><I>Drugs</i></b>
                    <form method= "get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>

                    <form method="get" action="searchDrug">
                        <input type ="submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>

                    <B><I>Companies</i></b>
                    <form method= "get" action="listCompanies">
                        <input type = "submit" value="Company list">
                        </input>
                    </form>

                    <form method="get" action="searchCompany">
                        <input type ="submit" value="Company Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <B><I>Warning list</i></b>
                    <form method= "get" action= "listWarnings">
                        <input type = "submit" value="Warnings list">
                        </input>
                    </form>
                    <a href="http://api.fda.gov/drug/label.json">Data Source</a>
                    <img src="https://s3.amazonaws.com/poly-screenshots.angel.co/Project/a1/502691/ade7e3af4d1b15412a068de5075a601f-original.png" alt="Logotipo de HTML5" width="280" height="78" align="right">
                </body>
            <html>"""
        return html
    #Aqui trabajamos con lo que hara una vez se haya metido en uno de los inputs. En el marco superior de la pesta;a del navegador saldra JGalant App
    def web_secundaria (self, lista):
        list_html ="""
                                <html>
                                    <head>
                                        <title>JGalant App</title>
                                        <a href="/">Home</a>
                                    </head>
                                    <body>

                            """
        #Creamos un iterador para cada informacion que extraiga de la pagina.
        #Para la visibilidad, con el ul y el li, cada dato ira diferenciado con un separador circular
        for item in lista:
            list_html += "<ul><li type=circle>" + item + "</li></ul>"

        list_html += """

                                    </body>
                                </html>
                            """
        return list_html
    #Definimos una nueva clase y pones limite por defecto 10
    def give_generic_results (self, limit=10):
        connector= http.client.HTTPSConnection(self.OPENFDAURL) #Establecemos la conexion y obtenemos respuesta.
        connector.request("GET", self.OPENFDAPATH + "?limit=" + str(limit))
        print(self.OPENFDAPATH +"?limit=" + str(limit))
        r1 = connector.getresponse()
        datos_noprocesados = r1.read().decode("utf8")
        datos= json.loads(datos_noprocesados)
        resultados= datos["results"] #En la lista de resultados guardamos todos los datos de results del OpenFDA, nos servira en adelante
        return resultados

    def cabeceras(self): #Ya que repetiremos mucha esta estructura en los futuros ifs que utilicemos, lo predefinimos para ahorrar espacio
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

    #Paso muy importante, trabajaremos con el url con esta funcion
    def do_GET(self):
        list_source = self.path.split("?") #Del Buscador, dividimos en dos partes (ya que solo puede haber un ?), y trabajamos con lo que esta a la derecha de la interrogacion
        if len(list_source) > 1:
            parametres = list_source[1]
        else:
            parametres = ""

        limit = 10

        if parametres:
            parse_limit = parametres.split("=") #Dentro de lo que esta a la derecha del ?, dividimos otra vez en dos partes para asi obtener por una parte 'limit' y por otra su valor. Asi establecemos el limite
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("limit: {}".format(limit))

        else:
            print("SIN PARAMERTROS")


        #Empezamos a trabajar ahora con que sucede si el cliente se mete en cada uno de los inputs
        if self.path =="/": #En caso de que cargue la pagina, imprime el servidor
            self.cabeceras()
            html=self.get_server()
            self.wfile.write(bytes(html, "utf8"))
        elif "listDrugs" in self.path: #Si elige listDrugs:
            self.cabeceras()
            lista_medicamentos = []
            resultados = self.give_generic_results(limit)
            for resultado in resultados:
                if ("generic_name" in resultado["openfda"]): #Dentro de la lista resultados definida previamente lee lo que hay en generic_name, si no hay generic_name pone Desconocido
                    lista_medicamentos.append (resultado["openfda"]["generic_name"][0])
                else:
                    lista_medicamentos.append("Desconocido")
            resultado_html = self.web_secundaria (lista_medicamentos)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif "listCompanies" in self.path: #Si se mete en ListCompanies:
            self.cabeceras()
            lista_companies = []
            resultados = self.give_generic_results(limit)

            for resultado in resultados: #De la lista resultados lee manufacturer_name y lo imprime posteriormente en la web_secundaria
                if("manufacturer_name" in resultado["openfda"]):
                    lista_companies.append(resultado["openfda"]["manufacturer_name"][0])
                else:
                    lista_companies.append("Desconocido")
            resultado_html = self.web_secundaria(lista_companies)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif "listWarnings" in self.path: #Una de las extensiones, lista de Warnings que tambien se encuentra en openfda y lee de isma manera que con las previas opciones
            self.cabeceras()
            lista_warnings = []
            resultados = self.give_generic_results(limit)
            for resultado in resultados:
                if ("warnings" in resultado):
                    lista_warnings.append(resultado["warnings"][0])
                else:
                    lista_warnings.append("Desconocido")
            resultado_html = self.web_secundaria(lista_warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif "searchDrug" in self.path: #Aqui es ligeramente distinto, ahora se mete en el buscador y busca un medicamento especifico
            self.cabeceras()
            limit = 10
            drug = self.path.split("=")[1]
            drugs = []
            connector= http.client.HTTPSConnection(self.OPENFDAURL) #Establece conexion con la pagina y busca el medicamento y obtiene resultados
            connector.request("GET", self.OPENFDAPATH + "?limit=" +str(limit) + self.OPENFDADRUG + drug)
            print(self.OPENFDAPATH + "?limit=" +str(limit) + self.OPENFDADRUG + drug)
            r1= connector.getresponse()
            data1 = r1.read()
            datos = data1.decode("utf-8")
            biblioteca_data = json.loads(datos)
            path_search_drug = biblioteca_data["results"]
            for resultado in path_search_drug:
                if ("generic_name" in resultado["openfda"]):
                    drugs.append(resultado["openfda"]["generic_name"][0])
                else:
                    drugs.append("Desconocido")

            resultado_html = self.web_secundaria(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif "searchCompany" in self.path: #Por ultimo, en caso de que escoga searchCompany(proceso casi identico al de searchDrug solo que le pide otra cosa tras la conexion a la web):
            self.cabeceras()
            limit= 10
            company= self.path.split("=")[1]
            companies = []
            conn = http.client.HTTPSConnection(self.OPENFDAURL)
            conn.request("GET", self.OPENFDAPATH + "?limit=" +str(limit) + self.OPENFDACOMPANY + company)
            r1= conn.getresponse()
            data1 = r1.read()
            datos= data1.decode("utf-8")
            biblioteca_data= json.loads(datos)
            path_search_company = biblioteca_data["results"]
            for event in path_search_company:
                companies.append(event["openfda"]["manufacturer_name"][0])
            resultado_html = self.web_secundaria(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))
        #Trabaja con los errores, que son otras 2 extensiones
        #Existen diferentes tipos de errores. Mientras que los de la banda 300 son redirecciones, los de 400 son errores del cliente.
        #Aqui trabajamos para que en caso de que sucedan, la pagina imprima el error  o rediriga a la pagina principal del servidor
        elif "redirect" in self.path:
            print("Redirigimos pagina principal")
            self.send_response(301)
            self.send_header("Location", "http://localhost:" +str(PORT))
            self.end_headers()
        elif "secret" in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return

















socketserver.TCPServer.allow_reuse_address= True

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
