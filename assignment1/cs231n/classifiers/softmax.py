import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = np.max(y) + 1
  # print(num_train, num_classes)
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = X.dot(W)
  max_s = np.max(scores, axis = 1)
  exp_s = np.exp(scores - max_s.repeat(num_classes).reshape(num_train, num_classes))
  
  for i in range(num_train):
    denominator_sum = np.sum(exp_s[i])
    loss -= np.log(exp_s[i, y[i]] / denominator_sum)
   
    for j in range(num_classes):
      dW[:,j]+= (exp_s[i,j] / denominator_sum) * X[i]

    dW[:,y[i]] -= X[i]
  loss /= num_train
  loss += 0.5 * reg * np.sum(W*W)
  
  dW /= num_train
  dW += reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]

  scores=X.dot(W)
  maxLogC = np.max(scores,axis=1)
  maxLogC=np.reshape(np.repeat(maxLogC,num_classes),scores.shape )
  expScores=np.exp(scores+maxLogC)
  exp_correct_class_score = expScores[np.arange(num_train), y]

  #loss
  loss=-np.log(exp_correct_class_score/np.sum(expScores,axis=1))
  loss=sum(loss)/num_train
  loss+=0.5*reg*np.sum(W*W)

  #gradient
  expScoresSumRow=np.reshape(np.repeat(np.sum(expScores,axis=1),num_classes),expScores.shape )
  graidentMatrix=expScores/ expScoresSumRow
  
  graidentMatrix[np.arange(num_train),y]-=1
  dW = X.T.dot(graidentMatrix)
  # dW[np.arange(num_classes),y] -= X[y,]
  dW/=num_train
  dW+=reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

