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

def build_model(in_size, out_size, hidden_layers=2, nodes_per_layer=16):
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=[None, in_size])
    for i in range(hidden_layers):
        net = tflearn.fully_connected(net, nodes_per_layer)
    net = tflearn.fully_connected(net, out_size, activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    return model

def start_session():
    sess = tf.Session()
    return sess

def get_saver():
    saver = tf.train.Saver()
    return saver


if __name__ == '__main__':
    sess = start_session()
    model = build_model(10,2)
    sess.run(model)
    sess.close()
