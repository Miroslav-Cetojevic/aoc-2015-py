import hashlib
import itertools
import json
import math
import operator
import sys

import numpy as np

from collections import defaultdict
from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum, StrEnum
from functools import reduce
from heapq import heapify, heappop, heappush, heapreplace
from itertools import accumulate, pairwise
from numbers import Number
from operator import itemgetter
from pprint import pprint
from queue import PriorityQueue
from time import perf_counter_ns
from typing import Callable, NamedTuple, Sequence

from os.path import join

from solutions.day import Day
from support import next_permutation
