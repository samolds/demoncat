import svm
import random
import csv
import sys



def build_set_from_file(filename):
  dim = int(filename.split(".")[1]) + 1
  data = []
  with open(filename, 'rb') as csvfile:
    freader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in freader:
      point = [0] * dim
      for i in range(dim):
        element = row[i + 1].split(":")
        idx = int(element[0])
        point[idx] = float(element[1])

      data.append({
        "label": int(row[0]),
        "data": point
      })

  return data, dim



def test(examples, weights, C):
  good = 0.0
  for inst in examples:
    xi = inst['data']
    yi = inst['label']
    if yi * svm.dot_prod(weights, xi) <= 1:
      good = good + 1.0
  return "%.03f%%" % ((good / len(examples)) * 100.0)



def compute(train_fn, test_fn, epoch):
  trains, dim = build_set_from_file(train_fn)
  tests, dim2 = build_set_from_file(test_fn)

  if dim != dim2:
    print "dimensionality of training and test data must be equivalent"
    raise

  stats = ["Accuracy  \tC  \t\tLearn Rt  \tE(w)"]
  results = svm.svm(trains, dim, epoch)
  for i in range(5):
    r = results[i]
    correct = test(tests, r['weight'], r['C'])
    stats.append("%s  \t%.03f  \t\t%.03f  \t\t%.03f" % (correct, r['C'], r['r'], r['loss']))

  return stats



def problem3():
  pairs = {
    "orig": ['astro/original/train.4', 'astro/original/test.4'],
    "orig_tr": ['astro/original/train-transformed.14', 'astro/original/test-transformed.14'],
    "scal": ['astro/scaled/train.4', 'astro/scaled/test.4'],
    "scal_tr": ['astro/scaled/train-transformed.14', 'astro/scaled/test-transformed.14'],
    "data": ['data0/train0.10', 'data0/test0.10'],
  }

  for k in pairs:
    stats = compute(pairs[k][0], pairs[k][1], 10)
    print "%s and %s" % (pairs[k][0], pairs[k][1])
    for s in stats:
      print "\t%s" % s
    print "\n\n"



def problem3_final():
  pairs = {
    "orig": ['astro/original/train.4', 'astro/original/test.4'],
    "scal": ['astro/scaled/train.4', 'astro/scaled/test.4'],
  }
  
  trains = []
  tests = []

  for k in pairs:
    tr, dim = build_set_from_file(pairs[k][0])
    te, dim2 = build_set_from_file(pairs[k][1])

    if dim != dim2:
      print "dimensionality of training and test data must be equivalent"
      raise

    trains = trains + tr
    tests = tests + te

  stats = ["Accuracy  \tC  \t\tLearn Rt  \tE(w)"]
  results = svm.svm(trains, dim, 30)
  for i in range(5):
    r = results[i]
    correct = test(tests, r['weight'], r['C'])
    stats.append("%s  \t%.03f  \t\t%.03f  \t\t%.03f" % (correct, r['C'], r['r'], r['loss']))

  print "combined astro training sets vs combined astro testing sets at epoch = 30"
  for s in stats:
    print "\t%s" % s



def main(argv):
  if len(argv) != 2:
    print "usage:\n\tpython run.py <train_data> <test_data>"
    return

  train_fn = argv[0]
  test_fn = argv[1]

  stats = compute(train_fn, test_fn)
  for s in stats:
    print "\t%s" % s



if __name__ == '__main__':
  #main(sys.argv[1:])
  problem3()
  problem3_final()
