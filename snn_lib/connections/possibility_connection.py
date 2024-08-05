from snn_lib.connections.base_connection import AbstractConnection
from snn_lib.neuron_models.base_neuron_model import AbstractNeuron
import numpy as np
class PossibilityConnection(AbstractConnection):
    def __init__(self, pre_connection_neuron : AbstractNeuron, post_connection_neuron: AbstractNeuron, possibility = 0.02, weights = None):
        super().__init__()
        self.possbility = possibility
        self.pre_connection_neuron = pre_connection_neuron
        self.post_connection_neuron = post_connection_neuron
        self.weights = weights
        

    def backward(self, x):
        return self.W * x #self.W.T @ x

    def pseudo_update_states(self, u = None):
        self.cache_states(self.states)
        return self.cached_states

    def get_output(self, u):
        out = np.multiply(self.W, self.mask) * u
        return out #self.W @ u
    
    def initialize(self, W = None, maintain_weights = False):
        size = (self.post_connection_neuron.n_neuron, self.pre_connection_neuron.n_neuron)
        if not maintain_weights:
            if not (self.weights is None):
                W = self.weights
            else:
                W = np.random.rand(self.post_connection_neuron.n_neuron, self.pre_connection_neuron.n_neuron) 
            
            if W.shape[0] != size[0] or W.shape[1] != size[1]:
                raise ValueError
            self.W = W
            mask = np.random.rand(self.post_connection_neuron.n_neuron, self.pre_connection_neuron.n_neuron)
            mask[mask >= self.possbility] = 0
            self.mask = mask
        
        self._states = [0]
        self._cached_states = None