import tensorflow as tf
import numpy as np
import sys, os,cv2
from sklearn.utils import shuffle
from scipy.misc import imread,imresize
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from skimage.transform import resize
from imgaug import augmenters as iaa
import imgaug as ia
from scipy.ndimage import zoom

old_v = tf.logging.get_verbosity()
tf.logging.set_verbosity(tf.logging.ERROR)
from tensorflow.examples.tutorials.mnist import input_data
np.random.seed(789)

# ====== miscellaneous =====
# code from: https://github.com/tensorflow/tensorflow/issues/8246
def tf_repeat(tensor, repeats):
    """
    Args:

    input: A Tensor. 1-D or higher.
    repeats: A list. Number of repeat for each dimension, length must be the same as the number of dimensions in input

    Returns:

    A Tensor. Has the same type as input. Has the shape of tensor.shape * repeats
    """
    expanded_tensor = tf.expand_dims(tensor, -1)
    multiples = [1] + repeats
    tiled_tensor = tf.tile(expanded_tensor, multiples = multiples)
    repeated_tesnor = tf.reshape(tiled_tensor, tf.shape(tensor) * repeats)
    return repeated_tesnor
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
# ====== miscellaneous =====

# # data
# mnist = input_data.read_data_sets('../../Dataset/MNIST/', one_hot=True)
# x_data, train_label, y_data, test_label = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
# x_data_added,x_data_added_label = mnist.validation.images,mnist.validation.labels
# x_data = x_data.reshape(-1, 28, 28, 1)  # 28x28x1 input img
# y_data = y_data.reshape(-1, 28, 28, 1)  # 28x28x1 input img
# x_data_added = x_data_added.reshape(-1, 28, 28, 1)
#
# x_data = np.vstack((x_data,x_data_added))
# train_label = np.vstack((train_label,x_data_added_label))
# train_batch = np.zeros((60000,28,28,1))
# test_batch = np.zeros((10000,28,28,1))
#
# for x in range(len(x_data)):
#     train_batch[x,:,:,:] = np.expand_dims(imresize(x_data[x,:,:,0],(28,28)),axis=3)
# for x in range(len(y_data)):
#     test_batch[x,:,:,:] = np.expand_dims(imresize(y_data[x,:,:,0],(28,28)),axis=3)
#
# # print out the data shape and the max and min value
# print(train_batch.shape)
# print(train_batch.max())
# print(train_batch.min())
# print(train_label.shape)
# print(train_label.max())
# print(train_label.min())
# print(test_batch.shape)
# print(test_batch.max())
# print(test_batch.min())
# print(test_label.shape)
# print(test_label.max())
# print(test_label.min())


def np_sig(x): return 1.0/(1.0+np.exp(-x))
def d_np_sig(x): return np_sig(x) * (1.0 - np_sig(x))

class FNN_numpy():

    def __init__(self,inc,outc):
        self.w = np.random.randn(inc,outc)
        self.m,self.v = np.zeros_like(self.w),np.zeros_like(self.w)

    def feedforward(self,input):
        self.input = input
        self.layer = self.input.dot(self.w)
        self.layerA = np_sig(self.layer)
        return self.layerA

    def backprop(self,grad):
        grad_part_1 = grad
        grad_part_2 = d_np_sig(self.layer)
        grad_part_3 = self.input

        grad_middle = grad_part_1 * grad_part_2
        grad = grad_part_3.T.dot(grad_middle)
        grad_pass = grad_middle.dot(self.w.T)

        self.m = self.m * beta1 + (1.0-beta1) * grad
        self.v = self.v * beta2 + (1.0-beta2) * grad ** 2
        m_hat,v_hat = self.m/(1.-beta1),self.v/(1.-beta2)
        adam_mid = learning_rate / (np.sqrt(v_hat) + adam_e) * m_hat
        self.w = self.w - adam_mid
        return grad_pass

class whitening_layer():

    def __init__(self):
        self.moving_sigma = 0
        self.moving_mean = 0

    def feedforward(self,input):
        self.u = np.expand_dims(np.mean(input,axis=1),1)
        self.sigma = (input - self.u).dot((input - self.u).T) / batch_size
        self.eigenval,self.eigvector = np.linalg.eigh(self.sigma)
        self.U = np.diag(1. / np.sqrt(self.eigenval + white_e)).dot(self.eigvector.T)
        self.whiten = self.U.dot(input-self.u)
        self.zca = self.eigvector.dot(self.whiten)
        return self.zca

    def backprop(self,grad):
        pass


# hyper
batch_size = 100

learning_rate = 0.0001
beta1,beta2,adam_e = 0.9,0.999,1e-8
white_e = 1e-10

# class
l0 = FNN_numpy(784,256)
l1 = whitening_layer()

# graph
temp = np.ones((50,784))

layer0 = l0.feedforward(temp)
layer1 = l1.feedforward(layer0)




# -- end code --
