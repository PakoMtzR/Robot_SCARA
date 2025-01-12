import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class SerialMonitorFrame(ttk.Frame):
    def __init__(self, parent, serial_connection):
        super().__init__(parent)
        self.serial_connection = serial_connection

        self.entry_data = ttk.Entry(self)
        self.entry_data.grid(column=0, row=0, sticky="ew", padx=(0, 5))

        button_send = ttk.Button(self, text="Send", command=self.send_data)
        button_send.grid(column=1, row=0)

        scrolledtext_monitor = scrolledtext.ScrolledText(self)
        scrolledtext_monitor.grid(column=0, row=1, columnspan=2, sticky="ew", pady=5)

        self.grid_columnconfigure(0, weight=1)

    def send_data(self):
        data = self.entry_data.get().upper()
        self.serial_connection.send(data)   