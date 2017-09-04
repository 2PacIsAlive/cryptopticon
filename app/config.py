from params import *

class NetworkConfig(object):

    def __init__(self, json):
        self.json = json
        self.layers = [LayerConfig(x) for x in json["layers"]]


class LayerConfig(object):

    def __init__(self, layer):
        self.classmap = {
            "fully_connected": FullyConnectedLayerParams,
            "dropout": DropoutLayerParams,
            "convolution_3d": Conv3dLayerParams,
            "max_pooling_3d": MaxPool3dLayerParams,
            "regression": RegressionLayerParams
        }
        self.type = layer["type"]
        self.params = self.classmap[self.type](layer)
