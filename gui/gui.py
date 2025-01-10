import tkinter as tk
from tkinter import ttk

class BoardConnectionFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label_port = ttk.Label(self, text="Port:")
        label_port.grid(column=0, row=0, sticky="e")

        combobox_ports = ttk.Combobox(self)
        combobox_ports.grid(column=1, row=0, padx=5)

        button_scan_ports = ttk.Button(self, text="Scan")
        button_scan_ports.grid(column=2, row=0)

        label_board = ttk.Label(self, text="Board:")
        label_board.grid(column=0, row=1, sticky="e")

        entry_board = ttk.Entry(self)
        entry_board.grid(column=1, row=1, sticky="ew", padx=5)

        button_connect_device = ttk.Button(self, text="Connect")
        button_connect_device.grid(column=2, row=1) 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Robot Scara")
        self.create_widgets()
    
    def create_widgets(self):
        board_connection_frame=BoardConnectionFrame(self)
        board_connection_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # button_calibrate = ttk.Button(master=self, text="Calibrar")
        # button_calibrate.pack()

        self.notebook = ttk.Notebook(master=self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear el contenido de cada una de las pestañas.
        self.web_label = ttk.Label(self.notebook,
            text="www.recursospython.com")
        self.forum_label = ttk.Label(self.notebook,
            text="foro.recursospython.com")
        
        # Añadirlas al panel con su respectivo texto.
        self.notebook.add(self.web_label, text="Web", padding=20)
        self.notebook.add(self.forum_label, text="Foro", padding=20)

        # label_theta_1 = ttk.Label(master=self, text="Angulo 1: ", pad=(5))
        # label_theta_2 = ttk.Label(master=self, text="Angulo 2: ", pad=(5))
        # label_theta_3 = ttk.Label(master=self, text="Angulo 3: ", pad=(5))
        # label_theta_1.grid(column=0, row=1)
        # label_theta_2.grid(column=0, row=2)
        # label_theta_3.grid(column=0, row=3)

        # spinbox_1 = ttk.Spinbox(master=self, from_=-200, to=200, increment=1)
        # spinbox_1.grid(column=1, row=1)
        # spinbox_2 = ttk.Spinbox(master=self, from_=-200, to=200, increment=1)
        # spinbox_2.grid(column=1, row=2)
        # spinbox_3 = ttk.Spinbox(master=self, from_=-200, to=200, increment=1)
        # spinbox_3.grid(column=1, row=3)
        
        # button_send = ttk.Button(master=self, text="Enviar", pad=10)
        # button_send.grid(column=0, row=4, columnspan=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()

    