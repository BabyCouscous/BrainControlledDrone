from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import scipy.io as sio
import numpy as np
import util
import matplotlib.pyplot as plt
from sklearn.externals import joblib


NN = joblib.load('NN_2.pkl')
scaler = joblib.load('scaler_2.pkl')


'''
test_data = scaler.transform(test_data)

prediction = NN.predict(test_data)
print(prediction)
'''

#print(NN)
#print(scaler)
'''
L_channel = util.sample_gen(2)
R_channel = util.sample_gen(2)

features = util.extraction(L_channel, R_channel)
print(features)
features = scaler.transform(features)
print(features)

prediction = NN.predict(features)
print(prediction)


plt.figure(1)
plt.subplot(2,1,1)
plt.plot(L_channel[0,:])
plt.title('Left Channel')

plt.subplot(2,1,2)
plt.plot(R_channel[0,:])
plt.title('Right Channel')

plt.show()
'''

samples = 100
class_types = 7
#prediction = np.zeros((1,samples*class_types))
err = 0
for i in range(class_types):
	for j in range(samples):
		prediction = np.zeros((1,7))
		L_channel = util.sample_gen(i)
		R_channel = util.sample_gen(i)

		features = util.extraction(L_channel, R_channel)
		features = scaler.transform(features)
		prediction = NN.predict(features)
		if prediction[0,i] != 1:
			err = err + 1


#print(prediction)
print(err)
print(1 - (err*1.00/1400))
