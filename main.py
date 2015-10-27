#!/usr/bin/env python
# Author: Sam Olds


from utilities.util import KNN
import sgmllib
import sys
import os


def build_sets_from_directory(directory, prefix, suffix, limit=None):
  parses = []
  for fn in os.listdir(directory):
    if prefix in fn and suffix in fn and limit != 0:
      parser = sgmllib.SGMLParser()
      with open(directory + "/" + fn, 'r') as f:
        parser.feed(f.read())
      parses.append(parser)
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

  parses = build_sets_from_directory(argv[0], "reut2-0", ".sgm", limit)

  x = parses[0]
  print dir(x)
  import pdb; pdb.set_trace()





if __name__ == '__main__':
  main(sys.argv[1:])
