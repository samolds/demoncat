# DemonCat
A Machine Learning sentence classifier. I plan to make something sweet using the following:
* A [web portal](http://demonc.at)
* The [Reuters-21578](http://www.daviddlewis.com/resources/testcollections/reuters21578/) dataset.
* MIT's [ConceptNet](http://conceptnet5.media.mit.edu/)


### Development Setup

```
git clone http://github.com/samolds/demoncat.git
virtualenv --no-site-packages demoncat
cd demoncat
source bin/activate
pip install -r requirements.txt
python main.py data
```
