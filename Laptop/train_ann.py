import numpy as np 
import matplotlib.pyplot as plt 
from scipy.io import loadmat

data = np.load('/home/kv/Git/AutoCar/Laptop/Training_data/data.npz')
train = data['train']
labels = data['labels']

#get the details about the data
print 'Details of the data set: '
print 'Input pixels shape: ', train.shape
print 'Output commands shape: ', labels.shape

#sigmoid 
def sigmoid(z):
	#print 'In sigmoid...shape : ', z.shape
	#print z[0, 0:5]
	#print (1 / (1 + np.exp(-z[0, 0:5])))
	return (1 / (1 + np.exp(-z)))

#vec2 = [-10, 0, 10]
#vec = np.array(vec2)
#print sigmoid(vec)
def forward_propagate(X, theta1, theta2):
	m = X.shape[0]
	#print 'X shape: ', X.shape
	#print 'theta1 shape: ', theta1.shape
	a1 = np.insert(X, 0, values=np.ones(m), axis=1)
	#print 'a1 layer shape: ', a1.shape
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


def cost_function(params, input_size, hidden_size, num_labels, X, y, alpha):
	m = X.shape[0]
	X = np.matrix(X)
	y = np.matrix(y)

	theta1 = np.matrix(np.reshape(params[0:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
	theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))

	a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

	#computing the cost
	J = 0
	for i in xrange(m):
		first_term = np.multiply(-y[i,:], np.log(h[i,:]))
		second_term = np.multiply((1 - y[i,:]), np.log(1 - h[i,:]))
		J += np.sum(first_term - second_term)

	J = J / m

	#add the reguralization term 
	reg = (float(alpha) / (2 * m)) * (np.sum(np.power(theta1[:,1:], 2)) + np.sum(np.power(theta2[:,1:], 2)))
	J += reg
	return J


#initialise the variables
input_size = 38400
hidden_size = 32
num_labels = 4
alpha = 1

params = (np.random.random(size=hidden_size * (input_size + 1) + num_labels * (hidden_size + 1)) - 0.5) * 0.25

m = train.shape[0]
X = np.matrix(train)
y = np.matrix(labels)

#print 'shape of the parameters for neural network: '
theta1 = np.matrix(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))  
theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))
#print 'theta1 shape: ', theta1.shape
#print 'theta2 shape: ', theta2.shape

#testing the above functions
#print '\n\nfeed forwarding through the neural network...'
#a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)
#print 'done with feed forwarding...'

#print '\n\ncalculating the cost...'
#J = cost_function(params, input_size, hidden_size, num_labels, X, y, alpha)
#print '\n\ncost at initial (randomized theta): ', J


def sigmoid_gradient(z):
	return np.multiply(sigmoid(z), (1-sigmoid(z)))


#apply the backprop
def backprop(params, input_size, hidden_size, num_labels, X, y, learning_rate):
	##### this section is identical to the cost function logic we already saw #####
    m = X.shape[0]
    X = np.matrix(X)
    y = np.matrix(y)

    # reshape the parameter array into parameter matrices for each layer
    theta1 = np.matrix(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
    theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))

    # run the feed-forward pass
    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

    # initializations
    J = 0
    delta1 = np.zeros(theta1.shape)  # (25, 401)
    delta2 = np.zeros(theta2.shape)  # (10, 26)

    # compute the cost
    for i in range(m):
        first_term = np.multiply(-y[i,:], np.log(h[i,:]))
        second_term = np.multiply((1 - y[i,:]), np.log(1 - h[i,:]))
        J += np.sum(first_term - second_term)

    J = J / m

    # add the cost regularization term
    J += (float(learning_rate) / (2 * m)) * (np.sum(np.power(theta1[:,1:], 2)) + np.sum(np.power(theta2[:,1:], 2)))

    ##### end of cost function logic, below is the new part #####

    # perform backpropagation
    for t in range(m):
        a1t = a1[t,:]  
        z2t = z2[t,:] 
        a2t = a2[t,:] 
        ht = h[t,:]  
        yt = y[t,:]  

        d3t = ht - yt  

        z2t = np.insert(z2t, 0, values=np.ones(1)) 
        d2t = np.multiply((theta2.T * d3t.T).T, sigmoid_gradient(z2t)) 

        delta1 = delta1 + (d2t[:,1:]).T * a1t
        delta2 = delta2 + d3t.T * a2t

    delta1 = delta1 / m
    delta2 = delta2 / m

    # add the gradient regularization term
    delta1[:,1:] = delta1[:,1:] + (theta1[:,1:] * learning_rate) / m
    delta2[:,1:] = delta2[:,1:] + (theta2[:,1:] * learning_rate) / m

    # unravel the gradient matrices into a single array
    grad = np.concatenate((np.ravel(delta1), np.ravel(delta2)))
    print 'Cost J:', J
    return J, grad

#perform back
J, grad = backprop(params, input_size, hidden_size, num_labels, X, y, alpha)

#print '\n\ncost after back prop: ', J
#print 'grad shape: ', grad.shape


from scipy.optimize import minimize

# minimize the objective function
fmin = minimize(fun=backprop, x0=params, args=(input_size, hidden_size, num_labels, X, y, alpha),
                method='TNC', jac=True, options={'maxiter': 100})
print fmin


X = np.matrix(train)  
theta1 = np.matrix(np.reshape(fmin.x[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))  
theta2 = np.matrix(np.reshape(fmin.x[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))


np.savez('/home/kv/Git/AutoCar/parameters.npz', theta1=theta1, theta2=theta2)
print 'done saving the parameters...'


#a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)  
#y_pred = np.array(np.argmax(h, axis=1) + 1)  
#y_pred  

#correct = [1 if a.all() == b.all() else 0 for (a, b) in zip(y_pred, y)]  
#accuracy = (sum(map(int, correct)) / float(len(correct)))  
#print 'accuracy = {0}%'.format(accuracy * 100)