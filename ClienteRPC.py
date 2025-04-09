import xmlrpc.client

# Clase que interactúa con el servidor RPC
class ClienteRPC:
    def __init__(self, servidor_url):
        self.servidor = xmlrpc.client.ServerProxy(servidor_url)

    def obtener_suma(self, a, b):
        return self.servidor.suma(a, b)

# Crear instancia del cliente RPC
cliente = ClienteRPC("http://localhost:8000/")

# Realizar la llamada remota a la función suma con 5 y 3
resultado = cliente.obtener_suma(9, 8)

# Imprimir el resultado recibido del servidor
print(f"Resultado de la suma: {resultado}")
