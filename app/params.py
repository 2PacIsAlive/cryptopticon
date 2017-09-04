class InputLayerParams(object):
    """
    Args:
        shape (list):
    """
    def __init__(self, params):
        self.shape = params["shape"]


class FullyConnectedLayerParams(object):
    """
    Args:
        num_units (int):
        activation (str):
    """
    def __init__(self, params):
        self.num_units = params["num_units"]
        self.activation = params["activation"]


class DropoutLayerParams(object):
    """
    Args:
        keep_prob (float):
    """
    def __init__(self, params):
        self.keep_prob = params["keep_prob"]


class Conv3dLayerParams(object):
    """
    Args:
        num_filters (int): Number of convolutional filters to use.
        filter_size (int): Size of each filter.
        activation (str): Activation function to use.
        """
    def __init__(self, params):
        self.num_filters = params["num_filters"]
        self.filter_size = params["filter_size"]
        self.activation = params["activation"]


class MaxPool3dLayerParams(object):
    """
    Args:
        kernel_size (int):
        strides (int):
    """
    def __init__(self, params):
        self.kernel_size = params["kernel_size"]
        self.strides = params["strides"]


class RegressionLayerParams(object):
    """
    Args:
        optimizer (str):
        loss_fcn (str):
        learning_rate (float):
    """
    def __init__(self, params):
        self.optimizer = params["optimizer"]
        self.loss_fcn = params["loss_fcn"]
        self.learning_rate = params["learning_rate"]