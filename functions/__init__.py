import shlex
import sys
import signal
import subprocess
from random import random
from pathlib import Path
from os import kill
from math import floor
from time import sleep
from flask import request
from typing import Type, List
from threading import Thread
from .config import *
