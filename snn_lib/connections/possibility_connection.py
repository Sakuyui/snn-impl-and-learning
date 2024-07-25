from snn_lib.connections.base_connection import AbstractConnection
from snn_lib.neuron_models.base_neuron_model import AbstractNeuron
import numpy as np
class PossibilityConnection(AbstractConnection):
    def __init__(self, pre_connection_neuron : AbstractNeuron, post_connection_neuron: AbstractNeuron, possibility = 0.02, weights_initializer = None):
        super().__init__()
        self.possbility = possibility
        self.pre_connection_neuron = pre_connection_neuron
        self.post_connection_neuron = post_connection_neuron
        self.weights_initializer = weights_initializer
        

    def backward(self, x):
        return self.W * x #self.W.T @ x

    def pseudo_update_states(self, u = None):
        self.cache_states(self.states)
        return self.cached_states

    def get_output(self, u):
        return np.multiply(self.W, self.mask) * u #self.W @ u
    
    def initialize(self, W = None):
        size = (self.pre_connection_neuron.n_neuron, self.post_connection_neuron.n_neuron)
        W = np.random.random.rand(self.pre_connection_neuron.n_neuron, self.post_connection_neuron.n_neuron) if self.weights_initializer is None else self.weights_initializer(size)
        mask = np.random.random.rand(self.pre_connection_neuron.n_neuron, self.post_connection_neuron.n_neuron)
        mask[mask >= self.possbility] = 0
        self.W = W
        self.mask = mask
        
        self._states = [0]
        self._cached_states = None