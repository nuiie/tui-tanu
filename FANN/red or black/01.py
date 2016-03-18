from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
import numpy as np

tmp = np.loadtxt('train01.csv', delimiter=',')
target = tmp[:,0]
data = np.delete(tmp, np.s_[:1], axis=1)

gnb = GaussianNB()
y_pred = gnb.fit(data, target).predict(data)
print("Number of mislabeled points out of a total %d points : %d" % (data.shape[0],(target != y_pred).sum()))