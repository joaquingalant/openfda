import http.client
import json

headers = {"User-Agent": "http-client"}

REST_SERVIDOR= "api.fda.gov"
REST_RECURSO = "/drug/label.json"
CONSULTA= "/?search=active_ingredient:acetylsalicylic&limit=100"

connector = http.client.HTTPSConnection(REST_SERVIDOR)
connector.request("GET", REST_RECURSO + CONSULTA, None, headers)

response1 = connector.getresponse()
aspirina = response1.read().decode("utf-8")
connector.close()

aspirins = json.loads(aspirina)["results"]


for aspirin in aspirins:
    print("ID: ", aspirin["id"])
    if aspirin["openfda"]:
        manufacturer = aspirin["openfda"]["manufacturer_name"]
        print("FABRICANTE: ",manufacturer)
    else:
        print("Fabricante no disponible")
