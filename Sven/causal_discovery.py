#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from sklearn import linear_model
from itertools import combinations

# Einlesen der Daten
data = pd.read_csv('data.txt', sep=',')

N = data.shape[0]
A = np.array(data['A']).reshape(N, 1)
B = np.array(data['B']).reshape(N, 1)
C = np.array(data['C']).reshape(N, 1)
D = np.array(data['D']).reshape(N, 1)

# Correlation für n = 0
print("A,B: %s" % str(stats.pearsonr(A, B)))


# partielle Korrelation
def partial_correlation(a, b, C):
    regression = linear_model.LinearRegression()
    regression.fit(C, a)
    r_a = a - regression.predict(C)
    regression.fit(C, b)
    r_b = b - regression.predict(C)
    correlation_coefficient, _ = stats.pearsonr(r_a, r_b)
    return correlation_coefficient

variables = [(A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')]


def get_graph(variables):
    """
    Parameters
    ----------
    variables : list of tuples
        The first element of the tuple is a numpy array, the second one is a
        string

    Returns
    -------
    adjacency matrix
    """
    # create a fully connected graph
    adj = [[1 for j in range(len(variables))] for i in range(len(variables))]
    k = 0
    # todo
    # while X, Y in get_nodes()...
    return adj

# partielle Korrellation n = 1
#for k in range(len(variables) - 2):
for var1, var2, var3 in combinations(variables, 3):
    v1, n1 = var1
    v2, n2 = var2
    v3, n3 = var3
    print("%s_%s|%s: %0.2f" % (n1, n2, n3, partial_correlation(v1, v2, v3)))
