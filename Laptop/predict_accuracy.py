#from train_ann import forward_propagate
import numpy as np

#load the parameters
params = np.load('/home/kv/Git/AutoCar/parameters.npz')
theta1 = params['theta1']
theta2 = params['theta2']
theta1 = np.matrix(theta1)
theta2 = np.matrix(theta2)
print 'shape of theta1: ', theta1.shape
print 'shape of theta2: ', theta2.shape

#load the training data
data = np.load('/home/kv/Git/AutoCar/Laptop/Training_data/data.npz')
train = data['train']
y = data['labels']
X = np.matrix(train)
#y = np.matrix(labels)

def sigmoid(z):
	#print 'In sigmoid...shape : ', z.shape
	#print z[0, 0:5]
	#print (1 / (1 + np.exp(-z[0, 0:5])))
	return (1 / (1 + np.exp(-z)))


def forward_propagate(X, theta1, theta2):
	m = X.shape[0]
	#print 'X shape: ', X.shape
	#print 'theta1 shape: ', theta1.shape
	a1 = np.insert(X, 0, values=np.ones(m), axis=1)
	print 'a1 layer shape: ', a1.shape
	z2 = a1 * theta1.T 
	#print 'z2 shape: a1 * theta1.T: ', z2.shape
	a2 = np.insert(sigmoid(z2), 0, values=np.ones(m), axis=1)
	#print 'a2 layer shape: ', a2.shape
	#print 'theta2 shape: ', theta2.shape
	z3 = a2 * theta2.T
	#print 'z3 shape: a2 * theta2.T', z3.shape
	h = sigmoid(z3)


	#give some info
	#print 'a1 layer shape: ', a1.shape
	#print 'z2 shape: ', z2.shape
	#print 'a2 layer shape: ', a2.shape
	#print 'z3 shape: ', z3.shape
	#print 'h layer shape: ', h.shape

	return a1, z2, a2, z3, h


a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2) 
y_pred = np.array(np.argmax(h, axis=1) + 1)  

print 'shape of y: ', y.shape
print 'y_pred shape: ', y_pred.shape
#print y_pred
m = y_pred.shape[0]
new_y = np.zeros(m).astype(int)

for idx in xrange(m):
	for k in xrange(4):
		if y[idx][k] == 1:
			new_y[idx] = k+1


correct = [1 if a==b else 0 for (a, b) in zip(y_pred, new_y)]
accuracy = (sum(map(int, correct)) / float(len(correct)))

print 'accuracy = {0}%'.format(accuracy*100)
