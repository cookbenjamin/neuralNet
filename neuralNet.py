import numpy as np
from activation import Activation
from scipy import optimize


class NeuralNet(object):
    def __init__(self, input_layer_size=2, output_layer_size=1, hidden_layer_sizes=[3]):
        # HyperParameters
        self._input_layer_size = input_layer_size
        self._output_layer_size = output_layer_size
        self._hidden_layer_sizes = hidden_layer_sizes

        # Easy access HyperParameters
        self._layer_sizes = self.generate_layer_sizes()

        # Initialise random weights
        self._layer_weights = self.generate_layer_weights()

        # Empty storage for use during training
        self._activations = []
        self._layer_inputs = []
        self._input = None
        self._output = None
        self._costs = []

    def generate_layer_sizes(self):
        layer_sizes = list()
        layer_sizes.append(self._input_layer_size)
        layer_sizes += self._hidden_layer_sizes
        layer_sizes.append(self._output_layer_size)
        return layer_sizes

    def generate_layer_weights(self):
        layer_weights = list()
        for i, size in enumerate(self._layer_sizes[1:]):
                layer_weights.append(np.random.randn(self._layer_sizes[i], size))
        return layer_weights

    def predict(self, input_matrix):
        input_matrix = np.array(input_matrix)
        self._activations = [input_matrix]
        self._layer_inputs = [input_matrix]
        for layer_weight in self._layer_weights:
            self._layer_inputs.append(np.dot(self._activations[-1], layer_weight))
            self._activations.append(Activation.sigmoid(self._layer_inputs[-1]))
        return self._activations[-1]

    def cost(self, test_input, real_output):
        return 0.5 * sum((real_output - self.predict(test_input)) ** 2)

    def compute_gradients(self, test_input, test_output):
        test_input = np.array(test_input)
        test_output = np.array(test_output)
        deltas = list()
        slopes = list()
        error = -(test_output - self.predict(test_input))
        for i, (activation, inputs) in enumerate(zip(reversed(self._activations[:-1]), reversed(self._layer_inputs))):
            if i == 0:
                deltas.append(np.multiply(error, Activation.sigmoid_prime(inputs)))
            else:
                deltas.append(np.dot(deltas[-1], self._layer_weights[-i].T) * Activation.sigmoid_prime(inputs))
            slopes.append(np.multiply(activation.T, deltas[-1]))

        slopes = [slope.ravel() for slope in reversed(slopes)]
        return np.concatenate(slopes)

    def optimize_interfacer(self, weights, input, output):
        self.set_weights(weights)
        return self.cost(input, output), self.compute_gradients(input, output)

    def set_weights(self, new_weights):
        old_size = 0
        for i, (last_size, next_size) \
                in enumerate(zip(self._layer_sizes[:-1],
                                 self._layer_sizes[1:])):
            self._layer_weights[i] = \
                np.reshape(new_weights[old_size:old_size+next_size*last_size], (last_size, next_size))
            old_size += next_size*last_size

    def get_weights(self):
        return np.concatenate([weight.ravel() for weight in self._layer_weights])

    def train(self, inputs, outputs):
        self._costs = []
        self._input = inputs
        self._output = outputs
        weights = self.get_weights()
        optimize_settings = {
            'jac': True,
            'method': 'BFGS',
            'args': (inputs, outputs),
            'options': {
                'maxiter': 2000,
                'disp': False
            },
            'callback': self.set_weights
        }
        result = optimize.minimize(self.optimize_interfacer,
                                   weights,
                                   **optimize_settings)
        self.set_weights(result.x)