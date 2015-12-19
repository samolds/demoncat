from set_build import *
import math
import sys


def find_classes(data):
  classes = {}
  for entry in data:
    for c in entry['labels']:
      if not c in classes:
        classes.update({c: 0})
      classes[c] += 1
  return classes


def log_likelihood(l_probs, wgl_probs):
  llh = 0.0
  for label in wgl_probs:
    summed_prob = 0.0
    for prob in wgl_probs[label]:
      summed_prob += wgl_probs[label][prob]
    if label in l_probs:
      llh = llh + l_probs[label] + (-1.0 * math.log(summed_prob))
    else:
      llh = llh + (-1.0 * math.log(summed_prob))
  return llh


# attempted adaptation from PG 15 of
# http://www.kamalnigam.com/papers/emcat-mlj99.pdf
def naive_bayes_em(examples, classes, unlabeled):
  label_probs, word_in_class_probs = naive_bayes(examples, classes)

  examples = examples + unlabeled
  vocab = set()
  for entry in examples:
    for v in entry['vector']:
      vocab.add(v)

  last_llh = 0.0
  llh = log_likelihood(label_probs, word_in_class_probs)
  while llh - last_llh > 0.05:
    last_llh = llh

    # naive_bayes ----------
    for classj in classes:
      docsj = []
      for entry in examples:
        if classj in entry['labels']:
          docsj.append(entry)
      p_classj = (len(docsj) * 1.0) / (len(examples) * 1.0)
      label_probs.update({classj: p_classj})
      textj = []
      for entry in docsj:
        textj = textj + entry['vector']
      n = len(textj) * 1.0
      for wk in vocab:
        nk = textj.count(wk) * 1.0
        pwkclassj = (nk + 1.0) / (n + len(vocab) * 1.0)
        if wk in word_in_class_probs:
          word_in_class_probs[wk].update({classj: pwkclassj})
        else:
          word_in_class_probs.update({wk: {classj: pwkclassj}})
    # end naive_bayes -------------
    llh = log_likelihood(label_probs, word_in_class_probs)

  return label_probs, word_in_class_probs




def naive_bayes(examples, classes):
  vocab = set()
  for entry in examples:
    for v in entry['vector']:
      vocab.add(v)
  class_prob = {}
  word_given_class_prob = {}
  for classj in classes:
    docsj = []
    for entry in examples:
      if classj in entry['labels']:
        docsj.append(entry)
    p_classj = (len(docsj) * 1.0) / (len(examples) * 1.0)
    class_prob.update({classj: p_classj})
    textj = []
    for entry in docsj:
      textj = textj + entry['vector']
    n = len(textj) * 1.0
    for wk in vocab:
      nk = textj.count(wk) * 1.0
      pwkclassj = (nk + 1.0) / (n + len(vocab) * 1.0)
      if wk in word_given_class_prob:
        word_given_class_prob[wk].update({classj: pwkclassj})
      else:
        word_given_class_prob.update({wk: {classj: pwkclassj}})
  return class_prob, word_given_class_prob



def classify_with_nb(label_probs, word_in_class_probs, classes, example):
  max_label = ""
  max_probability = 0.0
  for label in classes:
    prob = label_probs[label]
    for v in example['vector']:
      if v in word_in_class_probs and label in word_in_class_probs[v]:
        prob = prob * word_in_class_probs[v][label]
    max_probability = max(max_probability, prob)
    if max_probability == prob:
      max_label = label
  return max_label



def print_accuracy(label, word_in_label, labels, test):
  correct = 0
  for entry in test:
    if classify_with_nb(label, word_in_label, labels, entry) in entry['labels']:
      correct += 1
  print correct / (len(test) * 1.0)



def execute(train_fn, test_fn, unlabeled_fn):
  train = build_set_from_json_dir(train_fn)
  test = build_set_from_json_dir(test_fn)
  unlabeled = build_set_from_text_file(unlabeled_fn)

  classes = find_classes(train + test)

  label_probs, word_in_class_probs = naive_bayes(train, classes)
  print "Supervised Naive Bayes             \t",
  print_accuracy(label_probs, word_in_class_probs, classes, test)

  label_probs, word_in_class_probs = naive_bayes_em(train, classes, [])
  print "Supervised Naive Bayes with EM     \t",
  print_accuracy(label_probs, word_in_class_probs, classes, test)

  label_probs, word_in_class_probs = naive_bayes_em(train, classes, unlabeled)
  print "Semi-Supervised Naive Bayes with EM\t",
  print_accuracy(label_probs, word_in_class_probs, classes, test)



def main(argv):
  if len(argv) != 3:
    print "usage:\tpython run.py <train_data> <test_data> <unlabeled_data>"
    return

  train_fn = argv[0]
  test_fn = argv[1]
  unlabeled_fn = argv[2]
  execute(train_fn, test_fn, unlabeled_fn)




if __name__ == '__main__':
  main(sys.argv[1:])
