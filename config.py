import hashlib
import itertools
import sys

import numpy as np

from collections import defaultdict
from copy import deepcopy
from enum import Enum, StrEnum
from itertools import pairwise
from numbers import Number
from time import perf_counter_ns
from typing import NamedTuple, Any

from os.path import join

from solutions.day import Day
