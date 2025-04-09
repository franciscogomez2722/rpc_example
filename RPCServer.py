import socket
import json

class Calculadora:
    """
    Clase que simula una calculadora con métodos matemáticos simples.
    """
    def suma(self, a, b):
        """
        Método que realiza la suma de dos números.
        
        Args:
            a (int, float): Primer número para la suma.
            b (int, float): Segundo número para la suma.
        
        Returns:
            int, float: Resultado de la suma de los dos números.
        """
        return a + b

class JsonRpcRequest:
    """
    Representa una solicitud JSON-RPC.

    Attributes:
        method (str): El nombre del método que se va a invocar.
        params (dict): Los parámetros que se pasan al método.
        id (str, int): Identificador único de la solicitud para que el cliente pueda correlacionar la respuesta.
    """
    def __init__(self, method, params, request_id):
        """
        Inicializa la solicitud JSON-RPC.

        Args:
            method (str): Nombre del método que se va a invocar.
            params (dict): Parámetros asociados al método.
            request_id (str, int): Identificador único de la solicitud.
        """
        self.method = method
        self.params = params
        self.id = request_id

class JsonRpcServer:
    """
    Servidor JSON-RPC que escucha en un puerto y maneja solicitudes RPC.
    """

    def __init__(self, host="localhost", port=8080):
        """
        Inicializa el servidor JSON-RPC.

        Args:
            host (str): Dirección del host donde se ejecutará el servidor (por defecto "localhost").
            port (int): Puerto en el que el servidor escuchará las solicitudes (por defecto 8080).
        """
        self.host = host
        self.port = port
        self.calculadora = Calculadora()  # Instancia de la clase Calculadora

    def handle_request(self, data):
        """
        Maneja las solicitudes entrantes, las procesa y genera una respuesta JSON-RPC.

        Args:
            data (str): Datos de la solicitud en formato JSON.

        Returns:
            str: Respuesta en formato JSON-RPC.
        """
        try:
            # Parsear la solicitud JSON
            request = json.loads(data)
            method = request.get("method")  # El nombre del método
            params = request.get("params", {})  # Parámetros para el método
            request_id = request.get("id")  # Identificador de la solicitud

            # Si el método es "suma", realizamos la operación
            if method == "suma":
                a = params.get("a")  # Primer parámetro
                b = params.get("b")  # Segundo parámetro
                result = self.calculadora.suma(a, b)  # Realizar la suma

                # Respuesta exitosa con el resultado
                response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }
            else:
                # Si el método no es reconocido, devolvemos un error
                response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": "Method not found"},
                    "id": request_id
                }

            # Devolver la respuesta como un string JSON
            return json.dumps(response)

        except Exception as e:
            # En caso de error interno, se devuelve un error general
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": "Internal error"},
                "id": None
            })

    def start(self):
        """
        Inicia el servidor JSON-RPC y escucha en el puerto especificado.
        Acepta conexiones entrantes de clientes y procesa las solicitudes recibidas.
        """
        # Crear un socket TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))  # Asocia el socket al host y puerto
        server_socket.listen(5)  # Comienza a escuchar (máximo 5 conexiones en cola)

        print(f"Servidor JSON-RPC escuchando en {self.host}:{self.port}")

        while True:
            # Espera a que un cliente se conecte
            client_socket, client_address = server_socket.accept()
            print(f"Conexion establecida con {client_address}")

            # Recibe datos del cliente
            data = client_socket.recv(1024).decode("utf-8")
            if data:
                print(f"Solicitud recibida: {data}")
                # Maneja la solicitud y obtiene la respuesta
                response = self.handle_request(data)
                # Envía la respuesta al cliente
                client_socket.sendall(response.encode("utf-8"))

            # Cierra la conexión con el cliente
            client_socket.close()

# Punto de entrada principal para ejecutar el servidor
if __name__ == "__main__":
    # Crear una instancia del servidor y comenzar a escuchar
    server = JsonRpcServer()
    server.start()

