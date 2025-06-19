import configparser
import platform

import logging

logger = logging.getLogger(__name__)

cfg = configparser.ConfigParser()
cfg.read("./config.ini")

machine = platform.machine()
logger.info(f"Running on machine: {machine}")

is_arm = platform.machine().startswith("aarch64")
if not is_arm:
    logger.warning("Not running on a Raspberry Pi, some features may not work.")
