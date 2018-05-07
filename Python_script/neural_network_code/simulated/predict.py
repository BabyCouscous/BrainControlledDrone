from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import scipy.io as sio
import numpy as np
import util
import matplotlib.pyplot as plt
from sklearn.externals import joblib

from Tkinter import Tk, Label, Button

class MyFirstGUI:
	def __init__(self, master):
        	self.master = master
       		master.title("Sample EEG Signal Generator")

		self.label = Label(master, text="Choose Type of EEG Signal.")
		self.label.pack()

		self.button_0 = Button(master, text="class_type_0", height=5, width=40, command=lambda: self.sample_gen(0))
		self.button_0.pack()

		self.button_1 = Button(master, text="class_type_1", height=5, width=40, command=lambda: self.sample_gen(1))
		self.button_1.pack()

		self.button_2 = Button(master, text="class_type_2", height=5, width=40, command=lambda: self.sample_gen(2))
		self.button_2.pack()

		self.button_3 = Button(master, text="class_type_3", height=5, width=40, command=lambda: self.sample_gen(3))
		self.button_3.pack()

		self.button_4 = Button(master, text="class_type_4", height=5, width=40, command=lambda: self.sample_gen(4))
		self.button_4.pack()

		self.button_5 = Button(master, text="class_type_5", height=5, width=40, command=lambda: self.sample_gen(5))
		self.button_5.pack()

		self.button_6 = Button(master, text="class_type_6", height=5, width=40, command=lambda: self.sample_gen(6))
		self.button_6.pack()

		self.close_button = Button(master, text="Close", height=5, width=40, command=master.quit)
		self.close_button.pack()


	def sample_gen(self,class_type):
		L_channel = util.sample_gen(class_type)
		R_channel = util.sample_gen(class_type)

		features = util.extraction(L_channel, R_channel)
		features = scaler.transform(features)
		prediction = NN.predict(features)
		
		#print('prediction is class type %d' % (prediction))

		#plt.figure(figsize=(8,10))
		plt.get_current_fig_manager().window.setGeometry(600,0,800,1000)

		plt.suptitle('The prediction is type %d EEG signal!' % (prediction), fontsize=14, fontweight='bold')
		plt.subplot(2,1,1)	
		
		plt.plot(L_channel[0,:])
		plt.title('Left Channel')

		plt.subplot(2,1,2)
		plt.plot(R_channel[0,:])
		plt.title('Right Channel')

		plt.show()







NN = joblib.load('NN_1.pkl')
scaler = joblib.load('scaler_1.pkl')

root = Tk()
root.geometry('400x800+0+0')
root.title('Sample EEG Signal Generator')
my_gui = MyFirstGUI(root)
root.mainloop()

'''
NN = joblib.load('NN_1.pkl')
scaler = joblib.load('scaler_1.pkl')



samples = 100
class_types = 7
prediction = np.zeros((1,samples*class_types))

L_channel = util.sample_gen(i)
R_channel = util.sample_gen(i)

features = util.extraction(L_channel, R_channel)
features = scaler.transform(features)
prediction[0,samples*i + j] = NN.predict(features)


#print(prediction)
print(err)
print(1 - (err*1.00/len(prediction[0,:])))
plt.plot(prediction[0,:],'r.')
plt.xlabel('samples')
plt.ylabel('prediction')
plt.show()
'''
