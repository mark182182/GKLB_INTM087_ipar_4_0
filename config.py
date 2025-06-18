import configparser
from contextlib import contextmanager
from functools import wraps
import platform

from env_var import read_env_var

cfg = configparser.ConfigParser()
cfg.read("./config.ini")

machine = platform.machine()
print(f"Running on machine: {machine}")

is_arm = platform.machine().startswith("aarch64")
if not is_arm:
    print("Not running on a Raspberry Pi, some features may not work.")
