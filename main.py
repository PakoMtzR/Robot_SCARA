from machine import Pin, PWM
import time

# Definimos los pines del encoder
encoder_pin_a = Pin(18, Pin.IN, Pin.PULL_DOWN)  # 18
encoder_pin_b = Pin(16, Pin.IN, Pin.PULL_DOWN)  # 16

# Definimos los pines para controlar direccion del motor
motor_input_a = Pin(10, Pin.OUT)
motor_input_b = Pin(11, Pin.OUT)

# Definimos pin para en control del PWM
pin_pwm = PWM(Pin(12), freq=50, duty_u16=0)

# Variables del encoder y PID
encoder_counter = 0
target_pulses = 800
kp = 1
kd = 0
ki = 0.2

# Variables para el cálculo del PID
previous_error = 0
integral = 0
previous_time = time.ticks_ms()

# Funcion para la lectura del encoder
def read_encoder(pin):
    global encoder_counter
    encoder_counter += 1 if encoder_pin_a.value() == encoder_pin_b.value() else -1
    print("encoder_counter:", encoder_counter)

# Funcion para configurar giro del motor
def set_motor(direction=0, pwm_percent_value=0):
    # Verificamos valor de porcentaje de pwm [0% - 100%]
    pwm_percent_value = max(0, min(100, pwm_percent_value))

    # Configurar valor del pwm
    pin_pwm.duty_u16((pwm_percent_value*65_535)//100)     

    if direction == 1:
        motor_input_a.on()
        motor_input_b.off()
    elif direction == -1:
        motor_input_b.on()
        motor_input_a.off()
    else:
        motor_input_a.off()
        motor_input_b.off()

# Controlador PID
def pid_control():
    global previous_error, integral, previous_time

    # Calcular el intervalo de tiempo (delta t)
    current_time = time.ticks_ms()
    delta_time = time.ticks_diff(current_time, previous_time)/1000 # Convertimos a segundos
    previous_time = current_time

    # Calculo del error
    error = target_pulses - encoder_counter
    integral += error*delta_time
    derivative = (error-previous_error) / delta_time if delta_time > 0 else 0
    previous_error = error

    # Calcular la señal de control
    control_signal = kp*error + ki*integral + kd*derivative
    pwm_value = abs(int(control_signal))
    direction = 1 if control_signal > 0 else -1

    # Ajustar el motor en función de la señal de control
    set_motor(direction, pwm_value)

# Configuración de interrupción para el encoder
encoder_pin_a.irq(trigger=Pin.IRQ_RISING, handler=read_encoder)

# Bucle principal
running = True
while running:
    pid_control()  # Ejecuta el PID en cada iteración
    time.sleep_ms(10)  # Pausa de 100 ms para darle tiempo al sistema