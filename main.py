import time
from motor_encoder import MotorEncoder
from interrupts import LimitSwitch

# Declaramos los motores con encoder
motor_1 = MotorEncoder(20, 21, 13, 15, 14)
motor_2 = MotorEncoder(19, 18, 10, 12, 11)
motor_3 = MotorEncoder(17, 16, 9, 7, 8)

# Configuramos valores de PID
motor_2.kp = 2
motor_3.kp = 2

# Declaramos angulos objetivos
target_degrees_1 = -360
target_degrees_2 = -100
target_degrees_3 = -200

switch_1 = LimitSwitch(0)

while True:
    # motor_1.pid_control(target_degrees_1)   # Ejecuta el PID en cada iteración
    motor_2.pid_control(target_degrees_2)
    # motor_3.pid_control(target_degrees_3)
    time.sleep_ms(10)                       # Pausa de 100 ms para darle tiempo al sistema