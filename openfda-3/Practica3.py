import http.client   #Importamos los modulos que necesitemos                                                                
import json                                                                                                                 
import socket                                                                                                               
                                                                                                                            
#Para ser coherente con los primeros ejercicios, repetimos el proceso realizado y damos nombre a las variables              
headers = {'User-Agent': 'http-client'}                                                                                     
SERVER = "api.fda.gov"                                                                                                      
RESOURCE = "/drug/label.json"                                                                                               
limit= "?limit=10"                                                                                                          
                                                                                                                            
connector= http.client.HTTPSConnection(SERVER) #Mismo proceso que primeros ejercicios. Se establece la conexion             
connector.request("GET", RESOURCE + limit, None, headers)                                                                   
                                                                                                                            
info_data = connector.getresponse()                                                                                         
medicines = info_data.read().decode("utf-8")                                                                                
connector.close()                                                                                                           
                                                                                                                            
results = json.loads(medicines)["results"]                                                                                  
                                                                                                                            
InfClient = "" #Lo creamos vacío para rellenarlo posteriormente con la información de los medicamentos                      
for medicine in results: #Iniciamos un bucle 'for' en el que introduciremos                                                 
    openfda = medicine["openfda"]                                                                                           
    if openfda: #En caso de que esté en openfda                                                                             
        brand_name = openfda["brand_name"] #Pasamos los datos a string para poder trabajar con ellos de forma más cómoda    
        brand_name = ",".join(brand_name)                                                                                   
                                                                                                                            
        substance_name = openfda["substance_name"] #Mismo proceso que con brand_name, igual con manufacturer_name           
        substance_name = ",".join(substance_name)                                                                           
                                                                                                                            
        manufacturer_name = openfda["manufacturer_name"]                                                                    
        manufacturer_name = ",".join(manufacturer_name)                                                                     
                                                                                                                            
        InfClient = InfClient + brand_name + "\t" + substance_name + "\t" + manufacturer_name + "\n"                        
    else: #En caso de que no esté, no tendremos en esa información y lo mostraremos en pantalla                             
        no_info = ("No avalaible information\n")                                                                            
        InfClient = InfClient + no_info                                                                                     
                                                                                                                            
                                                                                                                            
IP = ""     #IP vacía para que funcione en todos los dispositivos en la dirección 0.0.0.0:PORT                              
PORT = 8210                                                                                                                 
MAX_OPEN_REQUEST = 5                                                                                                        
                                                                                                                            
                                                                                                                            
def InfForClient(clientsocket):                                                                                             
                                                                                                                            
    contenido = """                                                                                                         
    <html>                                                                                                                  
    <h1>Medication list</h1>                                                                                                
    <p> Brand name (1) Substance name (2) Manufacturer name(3) <p>                                                          
    <body style="background-color: yellow">                                                                                 
    <pre> """ + InfClient + """                                                                                             
    </pre>                                                                                                                  
    </html>                                                                                                                 
    """                                                                                                                     
                                                                                                                            
    linea_inicial = "HTTP/1.1 200 OK\n" #Mismo servidor que el realizado en clase                                           
    cabecera = "Content-Type: text/html\n"                                                                                  
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))                                                   
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)                                             
    clientsocket.send(mensaje_respuesta)                                                                                    
                                                                                                                                                                                                                                                      
                                                                                                                            
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                            
serversocket.bind((IP, PORT)) #Sirve para enlazar el IP con el Puerto                                                       
serversocket.listen(MAX_OPEN_REQUEST) #Sirve para conexiones realizadas al socket                                           
                                                                                                                            
while True: #En caso de que funcione, se lanzará el servidor y se esperará a que se reciba la petición                      
    print("Waiting for the client on IP:", IP, " PORT:", PORT)                                                              
    (clientsocket, addressclient) = serversocket.accept()                                                                   
    print("Request received:", addressclient)                                                                               
    InfForClient(clientsocket)                                                                                              
    clientsocket.close()                                                                                                    
                                                                                                                            
