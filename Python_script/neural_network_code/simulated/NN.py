from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import scipy.io as sio
import pywt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib

mat_contents = sio.loadmat('training_seq.mat')
training_data = mat_contents['data']

#desired = np.repeat([0,1,2,3,4,5,6],200,axis=0)
#desired = np.repeat([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],
		#[0,0,1,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,1,0,0],
		#[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]],200,axis=0)
desired = np.zeros((1400,7))
for i in range(7):
		for j in range(200):
			desired[i*200+j,i] = 1


#print(desired)
#scaler = MinMaxScaler()
scaler = StandardScaler()
scaler.fit(training_data[0:1400,:])
training_data = scaler.transform(training_data)



NN = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(40,30,30,30,30,30,25,25,20,10,5), random_state=1)


NN.fit(training_data[0:1400,:], desired)

joblib.dump(NN, 'NN_2.pkl')
joblib.dump(scaler, 'scaler_2.pkl')
print('training finished!')

'''
prediction = NN.predict(training_data[200:400,:])
print(prediction)
#plt.plot(prediction,'o')
#plt.show()
err = 0
for i in range(len(prediction)):
	if prediction[i] != 2:
		err = err + 1

print((1 - err*1.00/len(prediction)))
'''


