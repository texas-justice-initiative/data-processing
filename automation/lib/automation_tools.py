'''Shared utilities for data cleaning.'''


import os
import tempfile


import datadotworld as dw
import numpy as np
import pandas as pd


class CleaningError(Exception):
    pass
