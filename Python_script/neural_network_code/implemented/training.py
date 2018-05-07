from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pywt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

training_data = np.zeros((1200,24))

training_data[0:300,:] = joblib.load('stationary_ex.pkl')
training_data[300:600,:] = joblib.load('blink_ex.pkl')
training_data[600:900,:] = joblib.load('ud_ex.pkl')
training_data[900:1200,:] = joblib.load('lb_ex.pkl')
#training_data[1200:1500,:] = joblib.load('rb_ex.pkl')



#PCA + SVM
desired = np.zeros((1200,1))
desired[300:600,0] = 1
desired[600:900,0] = 2
desired[900:1200,0] = 3
desired = desired.ravel()



X_train, X_test, Y_train, Y_test = train_test_split(training_data, desired, test_size = 0.1)

pca = PCA(4)
projected = pca.fit_transform(X_train)

clf = svm.SVC(kernel='rbf',degree=3, random_state=1)
clf.fit(projected,Y_train)

predictions = clf.predict(pca.fit_transform(X_test))
print(classification_report(Y_test,predictions))



'''
#SVM plots
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(projected[:300,0], projected[:300,1], c='b', label='class 1')
ax.scatter(projected[300:600,0], projected[300:600,1], c='r', label='class 2')
ax.scatter(projected[600:900,0], projected[600:900,1], c='y', label='class 3')
ax.scatter(projected[900:1200,0], projected[900:1200,1], c='g', label='class 4')
plt.legend(loc='upper left')
plt.xlabel('1st component')
plt.ylabel('2nd component')
plt.show()
'''





'''
#FFT + NN
desired = np.zeros((1200,4))
for i in range(4):
		for j in range(300):
			desired[i*300:i*300+300,i] = 1

X_train, X_test, Y_train, Y_test = train_test_split(training_data, desired, test_size = 0.1)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


#NN = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(40,30,25,20,10,5), max_iter=1000, verbose=10, random_state=1)

NN = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(8,7), max_iter=1000, verbose=0, random_state=1)



NN.fit(X_train, Y_train)

#joblib.dump(NN, 'NN.pkl')
#joblib.dump(scaler, 'scaler.pkl')
print('training finished!')

#predictions = NN.predict(X_test)
prob = NN.predict_proba(X_test)
predictions = np.zeros_like(prob)
predictions[np.arange(len(prob)), prob.argmax(1)] = 1

#print(predictions)

print(classification_report(Y_test,predictions))
'''






