import http.client #Importamos los módulos que necesitaremos
import json

headers = {"User-Agent": "http-client"} #Nombramos parametros de nuevo, en la CONSULTA ponemos limite=100, más allá de ese número saltará un error
REST_SERVIDOR= "api.fda.gov"
REST_RECURSO = "/drug/label.json"
CONSULTA= "/?search=active_ingredient:acetylsalicylic&limit=100"

connector = http.client.HTTPSConnection(REST_SERVIDOR) #Establecemos conexion, lo leemos e interpretamos en json
connector.request("GET", REST_RECURSO + CONSULTA, None, headers)

response1 = connector.getresponse()
aspirina = response1.read().decode("utf-8")
connector.close()

aspirins = json.loads(aspirina)["results"]

for aspirin in aspirins: #Encontramos aquellos con acetilsalicilico como ingrediente activo, e impriimos sus ID y fabricantes
    print("ID: ", aspirin["id"])
    if aspirin["openfda"]:
        manufacturer = aspirin["openfda"]["manufacturer_name"]
        print("FABRICANTE: ",manufacturer)
    else: #En caso de no disponer la información necesaria, se imprimirá un mensaje por pantalla con el siguiente mensaje:
        print("Fabricante no disponible")
