from snn_lib.neuron_models.base_neuron_model import AbstractNeuron
from typing import Callable, List
from numpy.typing import NDArray
import numpy as np

class FixedSpikeTrainNeuronModel(AbstractNeuron):
 
    def __init__(self, N, spikes, hyperparameters):
        super().__init__()

        ## Hyperparameters
        self.set_hyperparameters({
                'dt': hyperparameters.get('dt', 1e-4), 
                'simulation_time_duration': hyperparameters.get('simulation_time_duration', 1),
            })

        ## parameters
        self.N = N
        self.time_steps = (int)(np.ceil(self.simulation_time_duration / self.dt))
        self.spikes = spikes
        
        self.INDEX_NEURONS_V = 0
        self.INDEX_T = 1
        self.INDEX_TLAST = 2

        self.initialize_states()

    def _generate_spikes(self):
        spikes = np.where(np.random.rand(self.time_steps, self.N) < self.fr * self.dt, 1, 0)
        self.spikes = spikes
        print("Num. of spikes:", np.sum(spikes))
        print("Firing rate:", np.sum(spikes)/(self.N * self.simulation_time_duration))
        
    @property
    def dt(self):
        return self._hyperparameters['dt']
    
    @property
    def simulation_time_duration(self):
        return self._hyperparameters['simulation_time_duration']

    def reset_spikes(self, spikes):
        self.spikes = spikes
     
        
    def update_state(self, u = None):
        t = self.states[self.INDEX_T]
        t += 1
        neurons_v = self.spikes[t]
        self.set_cached_states([neurons_v, t])
        
    def initialize_states(self):
        self.set_cached_states([[], 0])
        self._states = self._cached_states
        
