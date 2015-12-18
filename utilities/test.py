from set_build import *
import operator
import urllib2
import random
import json
import sys
import os


CONCEPT_NET_BASE = "http://conceptnet5.media.mit.edu/data/5.4/c/en/"
UNUSEFUL = [
  "the", "a", "an",
  "and", "or",
  "is", "was",
  "because"
]


#build_set_from_json_dir
#build_set_from_text_file
#build_set_from_text_dir

def find_classes(data):
  w_size = 500
  w = {}
  w_sorted = []
  for entry in data:
    for xi in entry['vector']:
      if xi not in UNUSEFUL:
        length = len(w)
        if length < w_size and xi in w:
          w[xi] += 1
        elif length < w_size:
          w.update({xi: 1})
        else:
          w_sorted = sorted(w.items(), key=operator.itemgetter(1))
          w.pop(w_sorted[0][0])
          w.update({xi: 1})
  return w


# adapted from PG 15 of
# http://www.kamalnigam.com/papers/emcat-mlj99.pdf
def naive_bayes_em(data):




def main(argv):
  if len(argv) != 1:
    print "usage:\n\tpython run.py <train_data>"
    return

  train_fn = argv[0]
  #data = build_set_from_text_file(train_fn)
  data = build_set_from_json_dir(train_fn)


  x = find_classes(data)
  sorted_x = sorted(x.items(), key=operator.itemgetter(1))
  sorted_x.reverse()
  for i in range(10):
    print sorted_x[i]
  import pdb; pdb.set_trace()

  resp = json.loads(urllib2.urlopen(CONCEPT_NET_BASE + sorted_x[1][0]).read())
  import pdb; pdb.set_trace()


  # overview?
    # search through corpus and find x most popular (non article) words
    # these become my classes
    # if i had more time: using list of classes - use concept net to find strongly connected nodes indicating they're suitable topic words
    # go back through corpus (data is list of "vectors". each vector is an array of words in a sentence)
    # use naive bayes to learn classifiers
    # potentially find a way to change classifiers as new one emerge


    # word2vec and svm???



if __name__ == '__main__':
  main(sys.argv[1:])
















