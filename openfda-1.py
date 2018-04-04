import http.client
import json

#Programa1
headers= {"User-Agent" : "http-client"}
REST_NOMBRE_SERVIDOR = "api.fda.gov"
REST_NOMBRE_RECURSO = "/drug/label.json"
DEBUG = True

connector = http.client.HTTPSConnection("api.fda.gov")
connector.request("GET", REST_NOMBRE_RECURSO, None, headers)
print(" *Su mensaje de solicitud ha sido enviado* ")

response1 = connector.getresponse()
print(response1.status, response1.reason)

drugs_json = response1.read().decode("utf-8")
connector.close()
drugs = json.loads(drugs_json)

medicamento_info = drugs["results"][0]
print("ID: ", medicamento_info["id"])
print("PROPOSITO: ",medicamento_info["purpose"][0])
print("FABRICANTE: ",medicamento_info["openfda"]["manufacturer_name"][0])

#Programa2
