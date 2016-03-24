from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cPickle

tmp = np.loadtxt('train02.csv', delimiter=',')
target = tmp[:,0]
data = np.delete(tmp, np.s_[:1], axis=1)
print "data shape",data.shape
print 'target shape', target.shape
# print data[1], target[1]

clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(data, target)
with open('forest/forest02.pickle', 'wb') as f:
    cPickle.dump(clf, f)

# with open('forest/forest01.pickle', 'rb') as f:
    # forest2 = cPickle.load(f)

"""
y_pred = clf.fit(data, target).predict(data)
print("Number of mislabeled points out of a total %d points : %d" % (data.shape[0],(target != y_pred).sum()))
"""