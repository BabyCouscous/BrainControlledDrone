import numpy as np
import pywt
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import sys
import util
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


features = np.zeros((1200,6))
filename = 'stationary.pkl'
pkl = joblib.load(filename)
LEFT = pkl[0][0]
RIGHT = pkl[1][0]


for i in xrange(300):
		features[i,:] = util.extraction(LEFT[i],RIGHT[i])

filename = 'blink.pkl'
pkl = joblib.load(filename)
LEFT = pkl[0][0]
RIGHT = pkl[1][0]

'''
#sample plot
sig = LEFT[48]
[ca4, cd4, cd3, cd2, cd1] = pywt.wavedec(sig, 'db4', level=4)
f1 = np.mean(np.absolute(cd2))
f2 = np.mean(np.absolute(cd3))
f3 = np.mean(np.absolute(cd4))

f, ax = plt.subplots(3, 2)
ax[0, 0].plot(sig)
ax[0, 0].set_title('sample signal')
ax[0, 1].plot(cd1)
ax[0, 1].set_title('detail space 1')

ax[1, 0].plot(range(len(cd2)),cd2,'b-', range(len(cd2)), [f1]*len(cd2) ,'r-')
ax[1, 0].set_title('detail space 2')

ax[1, 1].plot(range(len(cd3)),cd3,'b-', range(len(cd3)), [f2]*len(cd3) ,'r-')
ax[1, 1].set_title('detail space 3')

ax[2, 0].plot(range(len(cd4)),cd4,'b-', range(len(cd4)), [f2]*len(cd4) ,'r-')
ax[2, 0].set_title('detail space 4')

ax[2, 1].plot(ca4)
ax[2, 1].set_title('approximate space 4')

plt.show()
'''


for i in xrange(300):
		features[300+i,:] = util.extraction(LEFT[i],RIGHT[i])

filename = 'ud.pkl'
pkl = joblib.load(filename)
LEFT = pkl[0][0]
RIGHT = pkl[1][0]


for i in xrange(300):
		features[600+i,:] = util.extraction(LEFT[i],RIGHT[i])

filename = 'lb.pkl'
pkl = joblib.load(filename)
LEFT = pkl[0][0]
RIGHT = pkl[1][0]


for i in xrange(300):
		features[900+i,:] = util.extraction(LEFT[i],RIGHT[i])


desired = np.zeros((1200,4))
for i in range(4):
		for j in range(300):
				desired[i*300:i*300+300,i] = 1

X_train, X_test, Y_train, Y_test = train_test_split(features, desired, test_size=0.1)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

NN = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5), max_iter=2000, verbose=0, random_state=1)
	
NN.fit(X_train, Y_train)

prob = NN.predict_proba(X_test)
predictions = np.zeros_like(prob)
predictions[np.arange(len(prob)), prob.argmax(1)] = 1
print(classification_report(Y_test,predictions))

