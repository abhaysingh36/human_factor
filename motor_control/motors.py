import RPi.GPIO as GPIO

class Motors:
    def __init__(self, pins):
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        self.pwms = [GPIO.PWM(pin, 50) for pin in pins]
        for pwm in self.pwms:
            pwm.start(0)

    def set_speeds(self, speeds):
        for pwm, speed in zip(self.pwms, speeds):
            pwm.ChangeDutyCycle(speed)

    def cleanup(self):
        for pwm in self.pwms:
            pwm.stop()
        GPIO.cleanup()
