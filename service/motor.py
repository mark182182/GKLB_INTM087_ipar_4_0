from config import is_arm
from models.motor import MotorThreshold, MotorEvent
from repos import motor_event_repo, motor_config_repo
from globals import motor_state, logged_in_user

import logging

logger = logging.getLogger(__name__)

if is_arm:
    from raspi.motor_pwm import MotorPWM


class MotorService:
    current_speed = 0

    def __init__(self, in1_pin, in2_pin, en_pin):
        if is_arm:
            self.motor = MotorPWM(in1_pin, in2_pin, en_pin)

        self.current_speed = self.get_threshold().speed_pct

    def set_threshold(self, threshold: MotorThreshold):
        motor_config_repo.set_threshold(threshold)

    def get_threshold(self) -> MotorThreshold:
        return motor_config_repo.get_threshold()

    def set_speed(self, speed):
        if is_arm:
            userId = logged_in_user.id
            logger.info(f"Setting motor speed to {speed}% for userId: {userId}")
            self.motor.set_speed(speed)
        motor_event_repo.insert_event(userId, MotorEvent.SET_SPEED, speed)

    def forward(self):
        if is_arm:
            userId = logged_in_user.id
            try:
                motor_state.is_running = True
                logger.info(f"Motor moving forward for userId: {userId}")
                self.motor.forward()
            except Exception as e:
                logger.error(f"Error occurred while moving motor forward: {e}")
            finally:
                motor_state.is_running = False
        motor_event_repo.insert_event(userId, MotorEvent.FORWARD)

    def backward(self):
        if is_arm:
            userId = logged_in_user.id
            try:
                motor_state.is_running = True
                logger.info(f"Motor moving backward for userId: {userId}")
                self.motor.backward()
            except Exception as e:
                logger.error(f"Error occurred while moving motor backward: {e}")
            finally:
                motor_state.is_running = False
        motor_event_repo.insert_event(userId, MotorEvent.BACKWARD)

    def stop(self):
        if is_arm:
            userId = logged_in_user.id
            try:
                logger.info(f"Motor stopping for userId: {userId}")
                self.motor.stop()
            except Exception as e:
                logger.error(f"Error occurred while stopping motor: {e}")
            finally:
                motor_state.is_running = False
        motor_event_repo.insert_event(userId, MotorEvent.STOP)

    def cleanup(self):
        if is_arm:
            self.motor.cleanup()
