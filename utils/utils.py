import os
from typing import Dict, Union


def read_env(file: Union[str, os.PathLike]) -> Dict[str, str]:
    env_vars = {}
    with open(file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, value = line.strip().split("=", 1)
            env_vars[key] = value
    return env_vars
