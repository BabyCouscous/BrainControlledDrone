import numpy as np
import pywt
import scipy.io as sio


fs = 160
dt = 1.0/fs
StopTime = 1
t = np.arange(0,StopTime - dt,dt)
n_var = 0.01
a_var = 0.01
f_var = 0.5
a = np.array([[0.8, 1, 0.8],[0.5, 1, 0.4],[1, 0.3, 0.5],[0.7, 0.8, 0.9],[0.5, 0.9, 1.2],[1, 0.7, 0.9],[0.5, 0.5, 1]])
f = np.array([[10, 15, 20],[11, 13, 25],[13, 18, 19],[8, 14, 21],[10, 13, 17],[12, 20, 22],[14, 16, 18]])


# generate EEG signal from one of 7 classes
def sample_gen(class_type):
	data = generate(a[class_type,:], a_var, f[class_type,:], f_var, n_var, t)
	return data


def generate(a,a_var,f,f_var,v,t):
	L = len(t)
	data = np.zeros((1,L))
	for i in range(len(a)):
		data = data + (a[i] + np.sqrt(a_var)*np.random.randn(1))*np.sin(2*np.pi*(f[i] + np.sqrt(f_var)*np.random.randn(1))*t + 2*np.pi*np.random.rand(1))
								
	data = data + np.sqrt(v)*np.random.randn(1,L)
	return data
										

def extraction(data_L, data_R):
	features = np.zeros((1,6))
	[ca4, cd4, cd3, cd2, cd1] = pywt.wavedec(data_L, 'db4', level = 4)
	features[0,0] = np.mean(np.absolute(cd2))
	features[0,1] = np.mean(np.absolute(cd3))
	features[0,2] = np.mean(np.absolute(cd4))

	[ca4, cd4, cd3, cd2, cd1] = pywt.wavedec(data_R, 'db4', level = 4)
	features[0,3] = np.mean(np.absolute(cd2))
	features[0,4] = np.mean(np.absolute(cd3))
	features[0,5] = np.mean(np.absolute(cd4))

	return features


# generate L samples for each class type
def gen_training_data(L):
	training_data = np.zeros((7*L,6))

	for class_type in range(7):
		for i in range(L):	
			L_ch = sample_gen(class_type)
			R_ch = sample_gen(class_type)
			training_data[class_type*L + i,:] = extraction(L_ch, R_ch)
	
	sio.savemat('training_seq.mat',{'data': training_data})
