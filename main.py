import time
from motor_encoder import MotorEncoder

motor = MotorEncoder(18, 16, 12, 10, 11)
target_degrees = -100

while True:
    motor.pid_control(target_degrees)     # Ejecuta el PID en cada iteración
    time.sleep_ms(10)               # Pausa de 100 ms para darle tiempo al sistema