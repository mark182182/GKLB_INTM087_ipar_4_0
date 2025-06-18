from config import is_arm
from repo.temp import TemperatureRepo
from smtp.smtp_client import smtp
import matplotlib.pyplot as plt
import base64
import threading
import time

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
        self.measurements_in_last_min = []
        self.running = False
        self.thread = None

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
            self.measurements_in_last_min.append(temp)
            if len(self.measurements_in_last_min) > 60:
                self.measurements_in_last_min.pop(0)
            threshold = self.motor_service.get_threshold()
            if threshold and temp >= threshold.critical_temp:
                logger.warning(f"Temperature critical: {temp:.1f}C, stopping motor.")
                self.motor_service.stop()
                self.lcd.print_on_lcd([f"Kritikus ho!", f"T={temp:.1f}C"])
                if len(self.measurements_in_last_min) == 60:
                    logger.info("Sending email notification for critical temperature.")
                    imageData = self._create_temperature_graph(
                        self.measurements_in_last_min
                    )
                    try:
                        smtp.send_mail_on_critical_temperature(
                            temperature=temp,
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                            userId=None,  # TODO: Replace with actual user ID if available
                            rfidValue=None,  # TODO: Replace with actual RFID value if available
                            imageData=imageData,
                        )
                    except Exception as e:
                        logger.error(f"Failed to send email notification: {e}")
            time.sleep(self.measurement_interval_secs)

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
