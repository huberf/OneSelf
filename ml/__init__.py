# This is intended to be a suite of common tools and functions
# for the machine learning functionality of the OneSelf project
# components.

# General 3rd party library imports
import json
import os

# Specific 3rd party library imports
from os import listdir

# Local imports
try:
    from utils import convo_reader
except ModuleNotFoundError:
    from clara.utils import convo_reader

# ML specific library imports
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
import random

