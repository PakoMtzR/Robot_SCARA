from machine import Pin

class LimitSwitch:
    def __init__(self, pin) -> None:
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.count = 0
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)
    
    def handle_interrupt(self, _):
        print("ajijoles ", self.count)
        self.count += 1
