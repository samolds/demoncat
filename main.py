#!/usr/bin/env python
# Author: Sam Olds


from utilities.util import KNN
import urllib2
import json
import sys
import os



CONCEPT_NET_BASE = "http://conceptnet5.media.mit.edu/data/5.4/"
example = "c/en/toast"



def build_sets_from_directory(directory, prefix, suffix, limit=None):
  parses = []
  for fn in os.listdir(directory):
    if prefix in fn and suffix in fn and limit != 0:
      with open(directory + "/" + fn, 'r') as f:
        parses.append(json.loads(f.read()))
      if limit:
        limit -= 1
  return parses



def main(argv):
  if len(argv) < 1:
    print "Please follow this usage: execute [dir-with-data] [optional-limit]"
    return

  limit = None
  if len(argv) > 1:
    limit = int(argv[1])

  parses = build_sets_from_directory(argv[0], "reuters-0", ".json", limit)
  resp = json.loads(urllib2.urlopen(CONCEPT_NET_BASE + example).read())
  import pdb; pdb.set_trace()






if __name__ == '__main__':
  main(sys.argv[1:])
