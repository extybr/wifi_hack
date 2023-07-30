import shlex
import sys
import signal
import subprocess
from pathlib import Path
from os import kill
from math import floor
from flask import request
from typing import Type, List
from .config import *
