from serial_connector import SerialConnector
import time

connector = SerialConnector()
connection_sucess = connector.connect("COM15", 9600)

if connection_sucess:
    connector.send("ON")
    time.sleep(2)
    connector.send("OFF")
    time.sleep(2)
    connector.disconnect()
