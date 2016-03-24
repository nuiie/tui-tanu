from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cPickle

tmp = np.loadtxt('train02.csv', delimiter=',')
target = tmp[:,0]
data = np.delete(tmp, np.s_[:1], axis=1)


with open('forest/forest02.pickle', 'rb') as f:
    clf = cPickle.load(f)

y_pred = clf.predict(data)
print("Number of mislabeled points out of a total %d points : %d" % (data.shape[0],(target != y_pred).sum()))