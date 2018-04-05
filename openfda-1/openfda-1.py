import http.client #Importamos los modulos que necesitaremos
import json

#Programa1:
headers= {"User-Agent" : "http-client"} #Nombramos parametros de informacion que vamos a utilizar para que quede más cómodo visualmente
REST_NOMBRE_SERVIDOR = "api.fda.gov"
REST_NOMBRE_RECURSO = "/drug/label.json"

connector = http.client.HTTPSConnection("api.fda.gov") #Establecemos la conexion
connector.request("GET", REST_NOMBRE_RECURSO, None, headers) #Enviamos un mensaje de solicitud
print(" *Su mensaje de solicitud ha sido enviado* ")

response1 = connector.getresponse() #Obtenemos la respuesta del servidor
print(response1.status, response1.reason) #Imprimos la respuesta traduciendola con status y reason (OPCIONAL, NO NECESARIO)

drugs_json = response1.read().decode("utf-8") #Leemos el contenido en json y lo transformamos en una cadena
connector.close()
drugs = json.loads(drugs_json) #Procesamos el contenido en json

medicamento_info = drugs["results"][0] #Encontramos los 3 datos de cada medicamento que buscamos y los imprimimos
print("ID: ", medicamento_info["id"])
print("PROPOSITO: ",medicamento_info["purpose"][0])
print("FABRICANTE: ",medicamento_info["openfda"]["manufacturer_name"][0])

#Programa2:

connector.request("GET", REST_NOMBRE_RECURSO + "?limit=10", None, headers) #Muy muy parceido comienzo Programa1
print("  *CONSULTA DE 10 MEDICAMENTOS*  ")
response2 = connector.getresponse()
print(response2.status, response2.reason)

drugs_json = response2.read().decode("utf-8")
connector.close()

drugs = json.loads(drugs_json)
drugs = drugs["results"]

for drug in drugs: #Imprimimos el ID de los 10 medicamentos consultados
    print("IDENTIFICADOR:",drug["id"])

