import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports



from serial_connection import SerialConnection
from board_connection_frame import BoardConnectionFrame     


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Robot Scara")
        self.serial_connection = SerialConnection()
        self.create_widgets()

    def create_widgets(self):
        board_connection_frame = BoardConnectionFrame(self, self.serial_connection)
        board_connection_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # self.notebook = ttk.Notebook(master=self)
        # self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # # Crear el contenido de cada una de las pestañas.
        # self.web_label = ttk.Label(self.notebook,
        #     text="www.recursospython.com")
        # self.forum_label = ttk.Label(self.notebook,
        #     text="foro.recursospython.com")
        
        # # Añadirlas al panel con su respectivo texto.
        # self.notebook.add(self.web_label, text="Direct Kinematics", padding=20)
        # self.notebook.add(self.forum_label, text="Inverse Kinematics", padding=20)

        # send_to_serial_frame = SerialMonitorFrame(self, self.serial_connection)
        # send_to_serial_frame.pack(fill=tk.BOTH, padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()