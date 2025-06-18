from config import is_arm
from models.motor import MotorThreshold, MotorEvent

import logging

logger = logging.getLogger(__name__)

if is_arm:
    from raspi.motor_pwm import MotorPWM


class MotorService:
    def __init__(self, in1_pin, in2_pin, en_pin, motor_event_repo):
        self.motor_event_repo = motor_event_repo
        if is_arm:
            self.motor = MotorPWM(in1_pin, in2_pin, en_pin)

    def set_threshold(self, threshold: MotorThreshold):
        self.motor_event_repo.set_threshold(threshold)

    def get_threshold(self):
        return self.motor_event_repo.get_threshold()

    def set_speed(self, speed, userId=None):
        if is_arm:
            logger.info(f"Setting motor speed to {speed}% for userId: {userId}")
            self.motor.set_speed(speed)
        self.motor_event_repo.insert_event(userId, MotorEvent.SET_SPEED, speed)

    def forward(self, userId=None):
        if is_arm:
            logger.info(f"Motor moving forward for userId: {userId}")
            self.motor.forward()
        self.motor_event_repo.insert_event(userId, MotorEvent.FORWARD)

    def backward(self, userId=None):
        if is_arm:
            logger.info(f"Motor moving backward for userId: {userId}")
            self.motor.backward()
        self.motor_event_repo.insert_event(userId, MotorEvent.BACKWARD)

    def stop(self, userId=None):
        if is_arm:
            logger.info(f"Motor stopping for userId: {userId}")
            self.motor.stop()
        self.motor_event_repo.insert_event(userId, MotorEvent.STOP)

    def cleanup(self):
        if is_arm:
            self.motor.cleanup()
