# coding=utf-8
import numpy as np
import math

def initialize_parameters(n_x,n_h,n_y):
    np.random.seed(1)
    W1 = np.identity(n_x)
    b1 = np.zeros((n_h, 1)) + np.random.rand()
    W2 = np.identity(n_x)
    b2 = np.zeros((n_y, 1)) + np.random.rand()

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters


def linear_forward(A, W, b):
    Z = np.dot(W, A) + b
    cache = (A, W, b)

    return Z, cache


def tanh(x):
    y1 = (math.e ** (x) - math.e ** (-x)) / (math.e ** (x) + math.e ** (-x))
    cache = x
    return y1, cache


def sigmoid(Z):
    A = 1/(1+np.exp(-Z))
    cache = Z
    return A, cache

def relu(Z):
    A = np.maximum(0, Z)
    cache = Z
    return A, cache


def linear_activation_forward(A_prev, W, b, activation):
    if activation == "sigmoid":

        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)

    elif activation == "relu":

        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)

    elif activation == "tanh":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = tanh(Z)

    cache = (linear_cache, activation_cache)
    return A, cache


def L_model_forward(X, parameters):
    caches = []
    A = X
    L = len(parameters) // 2  # number of layers in the neural network

    for l in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters['W' + str(l)], parameters['b' + str(l)], 'relu')
        caches.append(cache)

    AL, cache = linear_activation_forward(A, parameters['W' + str(L)], parameters['b' + str(L)], 'sigmoid')
    caches.append(cache)

    return AL, caches


def compute_cost(AL, Y):
    m = Y.shape[1]
    cost = - np.sum(np.multiply(Y, np.log(AL)) + np.multiply(1 - Y, np.log(1 - AL))) / m
    print(cost)
    cost = np.squeeze(cost)  # To make sure your cost's shape is what we expect (e.g. this turns [[17]] into 17).
    return cost


def linear_backward(dZ, cache):
    A_prev, W, b = cache
    m = A_prev.shape[1]
    dW = 1 / m * np.dot(dZ, A_prev.T)
    db = 1 / m * np.sum(dZ, axis=1, keepdims=True)

    dA_prev = np.dot(W.T, dZ)


    return dA_prev, dW, db

def sigmoid_backward(dA, cache):
    Z = cache
    s = 1 / (1 + np.exp(-Z))
    dZ = dA * s * (1 - s)
    # assert (dZ.shape == Z.shape)
    return dZ

def tanh_backward(dA, cache):
    Z = cache
    s1 = np.exp(Z) - np.exp(-Z)
    s2 = np.exp(Z) + np.exp(-Z)
    tanh = s1 / s2
    s = dA * (1 - tanh * tanh)
    return s

def relu_backward(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True)  # just converting dz to a correct object.
    dZ[Z <= 0] = 0
    # assert (dZ.shape == Z.shape)
    return dZ
    # When z <= 0, you should set dz to 0 as well.

def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache

    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    elif activation == "sigmoid":

        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    elif activation =="tanh":
        dZ = tanh_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db



def update_parameters(parameters, grads, learning_rate):


    L = len(parameters) // 2  # number of layers in the neural network

    for l in range(L):
        if l == 0:
            parameters["b" + str(l + 1)] -= learning_rate * grads['db' + str(l + 1)]
            continue
        parameters["W" + str(l + 1)] -= learning_rate * grads['dW' + str(l + 1)]
        parameters["b" + str(l + 1)] -= learning_rate * grads['db' + str(l + 1)]
    return parameters


