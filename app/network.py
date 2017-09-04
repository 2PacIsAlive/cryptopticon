from flask import jsonify
import logging
import json
from sys import argv
from tflearn import DNN
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_3d, max_pool_3d
from tflearn.layers.estimator import regression

from config import NetworkConfig

class NetworkList:

    def __init__(self, user):
        self.user = user

    def to_json(self):
        return jsonify([
            {
                "name": "AlexNet",
                "description": "Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet Classification with Deep Convolutional Neural Networks. NIPS, 2012.",
                "layers": [
                    {
                        "type": "convolution_3d",
                        "name": 'conv2d_1',
                        "num_units": 1024,
                        "activation": "relu",
                        "order": 0
                    }
                ],
                "deployed": False
            },
            {
                "name": "VGG",
                "description": "description for VGG",
                "layers": [
                    {
                        "type": "regression",
                        "name": 'Regression',
                        "optimizer": "fixme",
                        "loss_fcn": "fixme",
                        "learning_rate": 0.05,
                        "order": 0
                    }, {
                        "type": "fully_connected",
                        "name": 'Fully Connected',
                        "num_units": 1024,
                        "activation": "fixme",
                        "order": 1
                    }
                ],
                "deployed": False
            }
        ])

class NetworkBuilder(object):
    """
    Attributes:
        log (logging.Logger): The logger for this module.
        network (tflearn.Network): #TODO fixme
        funcmap (dict): A mapping from config strings to NetworkBuilder functions.
    """
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    def __init__(self, config):
        """Construct a network from a config object.
        Args:
            config (network.config): A config object.
        """
        self.funcmap = {
            "input": self.add_input_layer,
            "fully_connected": self.add_fully_connected_layer,
            "dropout": self.add_dropout_layer,
            "convolution_3d": self.add_conv_3d_layer,
            "max_pooling_3d": self.add_max_pool_3d_layer,
            "regression": self.add_regression_estimator
        }

        self.network = None
        self.config = config

    def add_input_layer(self, params):
        """
        Args:
            params (nethub.network.config.InputLayerParams): The parameters for this layer.
        """
        self.network = input_data(shape=params.shape)

    def add_conv_3d_layer(self, params):
        """
        Args:
            params (nethub.network.config.Conv3DLayerParams): The parameters for this layer.
        """
        self.network = conv_3d(self.network, params.num_filters, params.filter_size,
                               activation=params.activation)

    def add_max_pool_3d_layer(self, params):
        """
        Args:
            params (nethub.network.config.MaxPool3DLayerParams): The parameters for this layer.
        """
        self.network = max_pool_3d(self.network, params.kernel_size,
                                   strides=params.strides)

    def add_fully_connected_layer(self, params):
        """
        Args:
            params (nethub.network.config.FullyConnectedLayerParams): The parameters for this layer.
        """
        self.network = fully_connected(self.network, params.num_units,
                                       activation=params.activation)

    def add_dropout_layer(self, params):
        """
        Args:
            params (nethub.network.config.DropoutLayerParams): The parameters for this layer.
        """
        self.network = dropout(self.network, params.keep_prob)

    def add_regression_estimator(self, params):
        """
        Args:
            params (nethub.network.config.RegressionLayerParams): The parameters for this layer.
        """
        self.network = regression(self.network, optimizer=params.optimizer,
                                  loss_fcn=params.loss_fcn, learning_rate=params.learning_rate)

    def build(self, checkpoint_path, max_checkpoints, tensorboard_verbose):
        """

        Args:
            checkpoint_path (str):
            max_checkpoints (int):
            tensorboard_verbose (int):
        Returns:
            tflearn.DNN: A tflearn DNN object that can be used as an estimator.
        """
        for layer_config in self.config.layers:
            self.funcmap[layer_config.type](layer_config.params)

        return DNN(self.network, checkpoint_path=checkpoint_path,
                   max_checkpoints=max_checkpoints,
                   tensorboard_verbose=tensorboard_verbose)

    def to_json(self):
        return jsonify(self.config.json)


def main(args):
    user = args[0]
    network = json.loads(args[1])
    NetworkBuilder(NetworkConfig(network)) \
        .build("", 1, 0)

if __name__=='__main__': main(argv[1:])