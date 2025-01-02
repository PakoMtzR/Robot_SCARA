from machine import Pin, PWM
import time

class MotorEncoder:
    def __init__(self, encoder_pin_a:int, encoder_pin_b:int, pin_pwm:int, motor_input_a:int, motor_input_b:int) -> None:
        # Definimos los pines del encoder
        self.encoder_pin_a = Pin(encoder_pin_a, Pin.IN, Pin.PULL_DOWN)  # 18
        self.encoder_pin_b = Pin(encoder_pin_b, Pin.IN, Pin.PULL_DOWN)  # 16

        # Definimos los pines para controlar direccion del motor
        self.motor_input_a = Pin(motor_input_a, Pin.OUT)    # 10
        self.motor_input_b = Pin(motor_input_b, Pin.OUT)    # 11

        # Definimos pin para en control del PWM
        self.pin_pwm = PWM(Pin(pin_pwm), freq=2000, duty_u16=0)  # 12

        # Variables del encoder y PID
        self.encoder_counter = 0
        self.kp = 5
        self.kd = 0.1
        self.ki = 0
        self.previous_error = 0
        self.integral = 0
        self.previous_time = time.ticks_ms()

        # Configuración de interrupción para el encoder
        self.encoder_pin_a.irq(trigger=Pin.IRQ_RISING, handler=self.read_encoder)

    def read_encoder(self, pin) -> None:
        """
        Funcion para la lectura del encoder
        """
        self.encoder_counter += 1 if self.encoder_pin_a.value() == self.encoder_pin_b.value() else -1
        print("encoder_counter:", self.encoder_counter)

    def set_motor(self, direction:int=0, pwm_percent_value:int=0) -> None:
        """
        Funcion para configurar el sentido de giro del motor \n
        direction = [-1,1] \n
        pwm_percent_value = [0-100]%
        """
        # Verificamos valor de porcentaje de pwm [0% - 100%]
        pwm_percent_value = max(0, min(100, pwm_percent_value))

        # Configurar valor del pwm
        self.pin_pwm.duty_u16((pwm_percent_value*65_535)//100)     

        if direction == 1:
            self.motor_input_a.on()
            self.motor_input_b.off()
        elif direction == -1:
            self.motor_input_b.on()
            self.motor_input_a.off()
        else:
            self.motor_input_a.off()
            self.motor_input_b.off()

    # Controlador PID
    def pid_control(self, target_degrees:int) -> None:        
        # Calcular el intervalo de tiempo (delta t)
        current_time = time.ticks_ms()
        delta_time = time.ticks_diff(current_time, self.previous_time)/1000 # Convertimos a segundos
        previous_time = current_time

        # Calculamos la cantidad de pulsos necesarios para llegar al angulo deseado
        target_pulses = (target_degrees*495)//360

        # Calculo del error
        error = target_pulses - self.encoder_counter
        self.integral += error*delta_time
        derivative = (error-self.previous_error) / delta_time if delta_time > 0 else 0
        self.previous_error = error

        # Calcular la señal de control
        control_signal = self.kp*error + self.ki*self.integral + self.kd*derivative
        # print(control_signal)
        # pwm_value = abs(int(control_signal))
        pwm_value = max(0, min(100, abs(int(control_signal))))
        direction = 1 if control_signal > 0 else -1

        # Ajustar el motor en función de la señal de control
        self.set_motor(direction, pwm_value)
