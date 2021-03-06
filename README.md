# neuralNet

A super simple artificial neural network written from the ground up in python.

## Requirements

The code was written to be interpreted as [Python 3](https://www.python.org/downloads/release/python-351/).

This neural network depends upon both NumPy and SciPy. Both belong to the SciPy stack.
You can install them by following the [SciPy stack installation instructions](http://scipy.org/install.html#individual-packages).

## Usage

```
Import:
>>> from neuralNet import NeuralNet

>>> nn = NeuralNet()

>>> x = [[3, 5]]
>>> y = [[.75]]

Train:
>>> nn.train(x, y)

Predict:
>>> nn.predict(x)
[[.750000000]]
```
