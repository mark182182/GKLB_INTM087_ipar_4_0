import os
from dotenv import load_dotenv

path_to_env = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(path_to_env)


def read_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is not None:
        return value
    else:
        raise ValueError(f"{key} is not defined in the environment.")
