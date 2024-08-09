import os
from .utils import utils

env = utils.read_env("./env")
os.environ.update(env)
