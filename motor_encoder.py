from machine import Pin, PWM
import time

# Definimos los pines del encoder
encoder_pin_a = Pin(18, Pin.IN, Pin.PULL_DOWN)  # 18
encoder_pin_b = Pin(16, Pin.IN, Pin.PULL_DOWN)  # 16

# Definimos los pines para controlar direccion del motor
motor_input_a = Pin(10, Pin.OUT)
motor_input_b = Pin(11, Pin.OUT)

# Definimos pin para en control del PWM
pin_pwm = PWM(Pin(12), freq=2000, duty_u16=0)

# Variables del encoder 
encoder_counter = 0
target_pulses = 11*45

# Funcion para la lectura del encoder
def read_encoder(pin):
    global encoder_counter, running
    encoder_counter += 1 if encoder_pin_a.value() == encoder_pin_b.value() else -1
    print("encoder_counter:", encoder_counter)
    if encoder_counter >= target_pulses:
        set_motor()
        running = False

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

# Configuración de interrupción para el encoder
encoder_pin_a.irq(trigger=Pin.IRQ_RISING, handler=read_encoder)

# Bucle principal
running = True
set_motor(1,30)
while running:
    time.sleep_ms(10)  # Pausa de 100 ms para darle tiempo al sistema