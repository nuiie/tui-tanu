from sklearn import datasets
from sklearn import svm
import numpy as np

tmp = np.loadtxt('train01.csv', delimiter=',')
target = tmp[:,0]
data = np.delete(tmp, np.s_[:1], axis=1)

lin_clf = svm.LinearSVC()
lin_clf.fit(data, target) 
LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0)
dec = lin_clf.decision_function([[1]])
dec.shape[1]