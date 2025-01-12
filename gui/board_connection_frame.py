import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class BoardConnectionFrame(ttk.Frame):
    def __init__(self, parent, serial_connection):
        super().__init__(parent)
        # Mapeo de VID:PID a nombres de dispositivos
        self.device_map = {
            "VID:PID=2341:0043": "Arduino Uno",
            "VID:PID=2341:0042": "Arduino Mega",
            "VID:PID=2E8A:0005": "Raspberry Pi Pico",
            "1A86:7523": "CH340 USB-Serial (posiblemente un clon de Arduino)",
            # Agrega otros dispositivos aquí
        }
        # Lista para almacenar los dispositivos detectados
        self.devices = []

        # Alamacenar el objeto de la conexion serial
        self.serial_connection = serial_connection

        # Creamos los widgets
        label_port = ttk.Label(self, text="Port:")
        label_port.grid(column=0, row=0, sticky="e")

        self.combobox_ports = ttk.Combobox(self, state="readonly")
        self.combobox_ports.grid(column=1, row=0, padx=5)
        self.combobox_ports.bind("<<ComboboxSelected>>", self.update_board_name)

        button_scan_ports = ttk.Button(self, text="Scan", command=self.update_ports)
        button_scan_ports.grid(column=2, row=0)

        label_board = ttk.Label(self, text="Board:")
        label_board.grid(column=0, row=1, sticky="e")

        self.entry_board = ttk.Entry(self, state="readonly")
        self.entry_board.grid(column=1, row=1, sticky="ew", padx=5)

        self.button_connection_device = ttk.Button(self, text="Connect", command=self.toggle_connection)
        self.button_connection_device.grid(column=2, row=1) 

        label_baudrate = ttk.Label(self, text="Baudrate:")
        label_baudrate.grid(column=0, row=2, sticky="e")

        self.combobox_baudrate = ttk.Combobox(self, state="readonly", values=["9600", "115200"])
        self.combobox_baudrate.grid(column=1, row=2, sticky="ew", padx=5)
        self.combobox_baudrate.current(0)

        # Inicializar lista de puertos
        self.update_ports()

    def scan_ports(self):
        """Escanea los puertos disponibles y devuelve una lista de los nombres de los dispositivos"""
        ports = serial.tools.list_ports.comports()
        devices = []

        for port in ports:
            vid_pid = port.hwid.split(" ")[1]
            device_name = self.device_map.get(vid_pid, "Dispositivo desconocido")
            devices.append({
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid,
                "name": device_name
            })
        return devices
    
    def update_ports(self):
        self.devices = self.scan_ports()
        port_names = [device["device"] for device in self.devices]
        self.combobox_ports["values"] = port_names

        if port_names:
            self.combobox_ports.current(0)
            self.update_board_name()
        else:
            self.combobox_ports.set("No existen puertos disponibles")
            self.entry_board.config(state="normal")
            self.entry_board.delete(0, tk.END)
            self.entry_board.config(state="readonly")

    def update_board_name(self, event=None):
        selected_index = self.combobox_ports.current()
        if selected_index != -1:
            selected_device = self.devices[selected_index]
            self.entry_board.config(state="normal")
            self.entry_board.delete(0, tk.END)
            self.entry_board.insert(0, selected_device["name"])
            self.entry_board.config(state="readonly")
        else:
            self.entry_board.config(state="normal")
            self.entry_board.delete(0, tk.END)
            self.entry_board.config(state="readonly")

    def toggle_connection(self):
        if self.serial_connection.serial_connection is None:
            # Obtenemos los campos para la comunicacion serial
            selected_port = self.combobox_ports.get()
            selected_baudrate = self.combobox_baudrate.get()

            # Establecemos la comunicacion serial
            connection_sucess = self.serial_connection.connect(selected_port, selected_baudrate)
            if connection_sucess:
                self.button_connection_device["text"] = "Disconnect"
        else:
            disconnection_sucess = self.serial_connection.disconnect()
            if disconnection_sucess: 
                self.button_connection_device["text"] = "Connect"