import http.client
import json
import socket

headers = {"User-Agent" : "http-client"}
SERVIDOR = "api.fda.gov"
RECURSO = "/drug/label.json"
LIMIT = "?limit=10"
connector = http.client.HTTPSConnection(SERVIDOR)
connector.request("GET", RECURSO + LIMIT, None, header)

datos10 = connector.getresponse()
medicine = datos10.read().decode("utf-8")
connector.close()

results = json.loads(medicine)['results']
