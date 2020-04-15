import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


# noinspection PyAttributeOutsideInit
class Adaline(object):  # Modified Perceptron
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):
        # X = self.standardize(X)
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.cost_ = []
        for i in range(self.n_iter):
            net_input = self.net_input(X)
            output = net_input  # introduce activation function here; change introduced between output and input
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors ** 2).sum() / 2
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)

    def standardize(self, X):
        x_std = np.copy(X)
        x_std[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
        x_std[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()
        return x_std

    def plot_decision_regions(self, X, y, classifier, resolution=0.02):
        markers = ('s', 'x', 'o', '^', 'v')
        colors = ('red', 'blue', 'lightgreen', 'grey', 'cyan')
        cmap = ListedColormap(colors[:len(np.unique(y))])
        x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
        Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        Z = Z.reshape(xx1.shape)
        plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
        plt.xlim(xx1.min(), xx1.max())
        plt.ylim(xx2.min(), xx2.max())
        for idx, c1 in enumerate(np.unique(y)):
            plt.scatter(x=X[y == c1, 0],
                        y=X[y == c1, 1],
                        alpha=0.8,
                        c=colors[idx],
                        marker=markers[idx],
                        label=c1,
                        edgecolors='black')
