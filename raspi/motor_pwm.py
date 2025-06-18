# Logic for controlling a DC motor via L298N H-Bridge on Raspberry Pi
import RPi.GPIO as GPIO

DEFAULT_PWM_FREQUENCY_HZ = 1000


class MotorPWM:
    def __init__(self, in1_pin, in2_pin, en_pin):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.en_pin = en_pin
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.en_pin, DEFAULT_PWM_FREQUENCY_HZ)
        self.pwm.start(0)

    def set_speed(self, speed):
        """Set motor speed (0-10%).

        The maximum speed is 10% of the PWM duty cycle, in order to prevent overcurrent/overheating.

        Args:
            speed (int): Speed percentage (0-10).
        """
        self.pwm.ChangeDutyCycle(speed)

    def forward(self):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def backward(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
