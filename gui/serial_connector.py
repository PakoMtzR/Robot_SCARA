import threading
import serial

class SerialConnector:
    def __init__(self):
        self.serial_connection = None
        self.thread = None
        self.connection_active = False
    
    def connect(self, port, baudrate):
        try:
            # Intentamos establecer una conexion serial
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            self.connection_active = True

            # Inicializamos un nuevo hilo para leer datos del serial
            # self.thread = threading.Thread(target=self.read_serial, daemon=True)
            # self.thread.start()

            print("Conexión establecida.")
            return True
        
        except serial.SerialException as e:
            print(f"Error al conectar: {e}")
            return False

    def disconnect(self):
        try:
            if self.serial_connection is not None and self.serial_connection.is_open:
                self.serial_connection.close()
                self.serial_connection = None
                self.connection_active = False

            # Aseguramos que el hilo termine correctamente
            if self.thread and self.thread.is_alive():
                self.thread.join()
            
            print("Dispositivo desconectado.")
            return True
            
        except serial.SerialException as e:
            print(f"Error al desconectar: {e}")
            return False

    def send(self, data):
        if not (self.connection_active and self.serial_connection and self.serial_connection.is_open):
            print("No existe conexión serial activa.")
            return
        
        try:
            self.serial_connection.write(data.encode("utf-8"))
            print(f"Enviado: {data}")
        except serial.SerialException as e:
            print(f"Error al enviar: {e}")


    def read_serial(self):
        while self.connection_active:
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    print(data)

                except serial.SerialException as e:
                    print(f"Error al leer: {e}")
                    break
            else:
                break