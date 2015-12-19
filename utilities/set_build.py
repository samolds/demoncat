import operator
import urllib2
import json
import os


CONCEPT_NET_BASE = "http://conceptnet5.media.mit.edu/data/5.4/c/en/"
UNUSEFUL = [
  "the", "a", "an",
  "and", "or",
  "is", "was",
  "because"
]


def build_set_from_json_dir(file_dir):
  data = []
  files = os.listdir(file_dir)

  for filename in files:
    if filename.split(".")[1] == "json":
      with open(file_dir + "/" + filename, 'rb') as f:
        data = data + json.loads(f.read())

  for entry in data:
    if 'body' in entry:
      entry['body'] = entry['body'].lower().replace("\n", " ").replace("\t", " ").replace("  ", "")
    else:
      entry['body'] = ""

    entry['vector'] = entry['body'].split(" ")
    entry['labels'] = []
    if 'topics' in entry:
      entry['labels'] = entry['labels'] + entry['topics']
    #if 'places' in entry:
    #  entry['labels'] = entry['labels'] + entry['places']

  return data


def build_set_from_text_file(filename):
  data = []
  raw = ""

  if filename.split(".")[1] == "txt":
    with open(filename, 'rb') as f:
      raw = f.read()

  raw = raw.lower().replace("\n", " ").replace("\t", " ").replace("  ", "")
  for d in raw.split(". "):
    data.append({
      "raw": d,
      "vector": d.split(" "),
      "labels": []
    })

  return data


def build_set_from_text_dir(file_dir):
  data = []
  files = os.listdir(file_dir)

  for filename in files:
    if filename.split(".")[1] == "txt":
      with open(file_dir + "/" + filename, 'rb') as f:
        data = data + f.read()

  for entry in data:
    entry['raw'] = entry['raw'].lower().replace("\n", " ").replace("\t", " ").replace("  ", "")
    entry['body'] = entry['raw'].split(". ")
    entry['vector'] = []
    for sent in entry['body']:
      entry['vector'].append(sent.split(" "))

  return data



def find_classes_from_popular(data):
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
