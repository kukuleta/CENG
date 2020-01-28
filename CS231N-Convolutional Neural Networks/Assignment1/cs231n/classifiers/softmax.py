from builtins import range
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

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_samples = X.shape[0]
    class_numbers = W.shape[1]
    for i in range(X.shape[0]):
        class_scores = X[i].dot(W)
        class_scores -= np.max(class_scores)
        unnormalized_log_probs = np.exp(class_scores)
        normalization_factor = 1 / np.sum(unnormalized_log_probs)
        for c in range(class_numbers):
            prob = unnormalized_log_probs[c] * normalization_factor
            if c == y[i]:
                loss -= np.log(prob)
                dW[:, c] += (-1 + prob) * X[i]
            else:
                dW[:, c] += prob * X[i]
    loss /= num_samples
    loss += 0.5 * reg * np.sum(W * W)
    dW /= num_samples
    dW += reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

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
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_samples = X.shape[0]
    class_scores = X.dot(W)
    class_scores = np.exp(class_scores - np.max(class_scores, axis=1)[:, np.newaxis])
    probs = class_scores / np.sum(class_scores, axis=1)[:, np.newaxis]
    loss = -np.sum(np.log(probs[range(num_samples), y])) / num_samples + 0.5 * reg * np.sum(W*W)
    probs[np.arange(probs.shape[0]),y] -= 1
    dW = (X.T.dot(probs) / num_samples) + reg * W


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
