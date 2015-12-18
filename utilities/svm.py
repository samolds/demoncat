from operator import itemgetter
import random


def sign(value):
  if value < 0:
    return -1
  else:
    return 1


def dot_prod(veca, vecb):
  if len(veca) != len(vecb):
    raise
  result = 0
  for i in range(len(veca)):
    result += veca[i] * vecb[i]
  return result


def sgd(examples, dim, T, C, p):
  t = 0.0
  weights = [0.0] * dim
  random.seed("Sam Olds")
  for epoch in range(T):
    random.shuffle(examples)
    for inst in examples:
      xi = inst["data"]
      yi = inst["label"]
      rt = p / (1.0 + p * (t / C))
      if yi * dot_prod(weights, xi) <= 1:
        for i in range(dim):
          term1 = (1.0 - rt) * weights[i]
          term2 = rt * C * float(yi) * xi[i]
          weights[i] = term1 + term2
      else:
        for i in range(dim):
          weights[i] = (1.0 - rt) * weights[i]
      t = t + 1.0
  return weights


# loss function to minimize in svm
def loss_fn(examples, weights, C):
  w = 0.5 * dot_prod(weights, weights)
  total = 0.0
  for inst in examples:
    b = 1.0 - inst["label"] * dot_prod(weights, inst["data"])
    total = total + max(0.0, b)
  return w + C * total


def svm(examples, dim, epochs):
  # hyperparamters
  Cs = [0.001, 0.01, 0.1, 1.0, 10.0]
  Rs = [0.001, 0.01, 0.1, 1.0]

  # search for best weight vector
  bests = []

  # iterate through every example of 
  for c in Cs:
    for r in Rs:
      # calculate weight vector using stochastic gradient descent
      weights = sgd(examples, dim, epochs, c, r)
      
      # calculate loss (margin) to be minimized
      loss = loss_fn(examples, weights, c)
      bests.append({
        "weight": weights,
        "C": c,
        "r": r,
        "loss": loss,
      })

  sorted_bests = sorted(bests, key=itemgetter('loss'))
  return sorted_bests
