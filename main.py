import time
from motor_encoder import MotorEncoder
from interrupts import LimitSwitch

from machine import UART

# Configuración del puerto serial
uart = UART(0, baudrate=9600, tx=0, rx=1)

# Declaramos los motores con encoder
motor_1 = MotorEncoder(21, 20, 13, 14, 15)
motor_2 = MotorEncoder(18, 19, 10, 11, 12)
motor_3 = MotorEncoder(17, 16, 9, 7, 8)

# Configuramos valores de PID de los motores segun sea necesario
motor_2.kp = 2
motor_3.kp = 2
motor_3.kd = 0.2

# Declaramos angulos objetivos
target_degrees_1 = -1000
target_degrees_2 = -100
target_degrees_3 = 100

while True:
    if uart.any():  # Verifica si hay datos en el buffer de entrada
        data = uart.read()  # Lee los datos disponibles
        print("Datos recibidos:", data) 
    # data = input().strip().split(",")
    # print(data)
    # if data[0] == "D" and len(data) == 4:
    #     angle_values = [int(x) for x in data[1::]]
    # else:
    #     angle_values = [0 for _ in range(3)]
    # print(angle_values)

    # Ejecuta el PID en cada iteración
    # motor_1.pid_control(target_degrees_1) 
    # motor_1.pid_control(angle_values[0])   
    # motor_2.pid_control(angle_values[1])
    # motor_3.pid_control(angle_values[2])
    time.sleep_ms(10)                       # Pausa de 100 ms para darle tiempo al sistema