from config import is_arm
from repo.temp import TemperatureRepo
from smtp.smtp_client import smtp
import matplotlib.pyplot as plt
import base64
import threading
import time
from globals import motor_state

import logging

logger = logging.getLogger(__name__)

if is_arm:
    from raspi.temp_sensor import TempSensor
    from service.motor import MotorService
    from raspi.lcd_i2c import LcdI2c


class TemperatureService:
    def __init__(self, repo: TemperatureRepo):
        self.repo = repo
        if is_arm:
            self.sensor = TempSensor()

    def read_and_log_temperature(self):
        if is_arm:
            temp = self.sensor.read_temperature()
            self.repo.insert_temperature(temp)
            return temp


class TemperatureMonitor:
    def __init__(
        self, temp_service: TemperatureService, motor_service: MotorService, lcd: LcdI2c
    ):
        self.temp_service = temp_service
        self.motor_service = motor_service
        self.lcd = lcd
        self.measurement_interval_secs = 1
        self.measurements = []
        self.speed_down_threshold_pct = 0.2
        self.speed_up_threshold_pct = 0.1
        self.stop_threshold_pct = 0.5
        self.running = False
        self.thread = None
        self.last_email_time = 0

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _monitor(self):
        while self.running:
            temp = self.temp_service.read_and_log_temperature()
            self.measurements.append(temp)
            if len(self.measurements) > 30:
                self.measurements.pop(0)
            threshold = self.motor_service.get_threshold()
            if threshold and temp >= threshold.critical_temp:
                logger.warning(f"Temperature critical: {temp:.1f}C.")
                self._handle_threshold_logic(temp, threshold)
            else:
                logger.info(
                    f"Current temperature: {temp:.1f}C, below critical threshold."
                )
                self._apply_motor_speed_up(temp, threshold)
                if motor_state.is_running:
                    self.lcd.print_on_lcd(["Homerseklet:", f"{temp:.1f}C"])
            time.sleep(self.measurement_interval_secs)

    def _handle_threshold_logic(self, temp, threshold):
        temp_diff_pct = (threshold.critical_temp - temp) / threshold.critical_temp
        self._apply_gradual_motor_slowdown(temp_diff_pct, threshold)
        if motor_state.is_running:
            self.lcd.print_on_lcd([f"Kritikus ho!", f"T={temp:.1f}C"])
        now = time.time()
        if len(self.measurements) == 30 and (now - self.last_email_time > 600):
            logger.info("Sending email notification for critical temperature.")
            max_temp = max(self.measurements)
            self._send_critical_temperature_email(max_temp, self.measurements)

    def _apply_gradual_motor_slowdown(self, temp_diff_pct, threshold):
        if temp_diff_pct >= self.stop_threshold_pct:
            logger.warning(
                f"Temperature difference {temp_diff_pct:.1f}C exceeds stop threshold. Stopping motor."
            )
            self.motor_service.stop()
        elif temp_diff_pct >= self.speed_down_threshold_pct * 3:
            logger.warning(
                f"Temperature difference {temp_diff_pct:.1f}C is high, setting speed to 25%."
            )
            self.motor_service.set_speed(threshold.speed_pct * 0.25)
        elif temp_diff_pct >= self.speed_down_threshold_pct * 2:
            logger.warning(
                f"Temperature difference {temp_diff_pct:.1f}C is moderate, setting speed to 50%."
            )
            self.motor_service.set_speed(threshold.speed_pct * 0.5)
        elif temp_diff_pct >= self.speed_down_threshold_pct:
            logger.warning(
                f"Temperature difference {temp_diff_pct:.1f}C is low, setting speed to 75%."
            )
            self.motor_service.set_speed(threshold.speed_pct * 0.75)

    def _apply_motor_speed_up(self, temp, threshold):
        if temp < threshold.critical_temp * (1 - self.speed_up_threshold_pct):
            logger.info(
                f"Temperature {temp:.1f}C is below speed up threshold, increasing speed."
            )
            self.motor_service.set_speed(threshold.speed_pct * 1.2)

    def _send_critical_temperature_email(self, max_temp, measurements):
        imageData = self._create_temperature_graph(measurements)
        try:
            timestamp = time.time() - len(measurements) * self.measurement_interval_secs
            smtp.send_mail_on_critical_temperature(
                max_temp=max_temp,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
                userId=None,  # TODO: Replace with actual user ID if available
                rfidValue=None,  # TODO: Replace with actual RFID value if available
                imageData=imageData,
            )
            self.last_email_time = time.time()
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")

    def _create_temperature_graph(self, measurements: list[float]) -> str:
        """Create a temperature graph from the given measurements.

        Args:
            measurements (list[float]): The temperature measurements.

        Returns:
            str: the base64 encoded image data of the graph.
        """
        plt.clf()
        plt.plot(measurements, label="Hőmérséklet")
        plt.xlabel("Idő (s)")
        plt.ylabel("Hőmérséklet (°C)")
        plt.title("Hőmérséklet az idő függvényében")
        plt.legend()
        image_path = "/tmp/temp_graph.png"
        plt.savefig(image_path)
        plt.close()
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        return image_base64
