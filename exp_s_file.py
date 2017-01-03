import time
from model import Model 
from SPN2 import SPN
import numpy as np
import random
import sys
num = sys.argv[1]
mn = sys.argv[2]
minibatch_cap = 0
m_start = int(sys.argv[6])
factor = 2
step = float(sys.argv[5])
cf = float(sys.argv[4])
mem = True
m = 2024
r = 2
valid_losses = []
test_loss = 0
my_spn = SPN()
pbf = (50, 90)
sbf = (9, 13)
depth = 6
if cf == 0 and step == 0:
	print "oops"
	exit(0)
var_num = int(sys.argv[3])
#my_spn.make_fast_model_from_file('../Modelz/' + mn +'.spn.txt', random_weights=True, step=step)
my_spn.make_random_model((pbf, sbf), var_num, 1)#step=step)
my_spn.start_session()
my_size = len(my_spn.model.id_node_dict) + len(my_spn.model.input_order)
mylayers = len(my_spn.model.node_layers)
print len(my_spn.model.node_layers)
#my_spn.make_model_from_file('../spn_models/ + mn + .spncc.spn.txt', True)
# assert 1.1 >= my_spn.predict([[1]]*1574)[0][0]
my_spn.add_data('../Dataz/' + mn + '.ts.data', 'train', mem)
my_spn.add_data('../Dataz/' + mn + '.test.data', 'test')
#my_spn.add_data('../Dataz/docword.' + mn + '.valid.txt', 'valid')
# b = my_spn.test(my_spn.data.valid.T)
# my_spn.train(20)
i = 0
# for d in my_spn.data.valid.T[:100]:
# 	i += 1
# 	my_spn.model.apply_count([d])
# 	if i % 100 == 0:
# 		print str(i) + "/" + str(len(my_spn.data.valid.T))
# vloss = my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: my_spn.data.valid.T})
# print vloss
# valid_losses.append(vloss)
def myreshape(data, spn):
	n_data = data
	n_data = n_data[:, spn.input_order, 0:1]
	n_data = np.reshape(n_data, (len(n_data), n_data.shape[1]*n_data.shape[2]))
	return n_data

#print my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: myreshape(my_spn.data.test, my_spn)})

start = time.time()
print start
if not mem:
	data = my_spn.data.train.T
	a = 0
	ms = 20
	n = m
	for i in range(len(data)//ms+1):
		b = min(len(data), a + ms)
		if i == n:
			my_spn.model.normalize_weights()
		if i < n:
			my_spn.model.apply_count(data[a:b])
		if i < n:
			for p in range(r):
				my_spn.model.session.run(my_spn.model.opt_val, feed_dict = {my_spn.model.input: data[a:b]})
		if i % 1 == 0:
			print my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: my_spn.data.test.T})
		# else:
		# 	my_spn.model.session.run(my_spn.model.opt_val2, feed_dict = {my_spn.model.input: data[a:b]})
		a += ms
		if ms < minibatch_cap:
			ms *= 1.6
			ms = int(ms)
		print i
		if a > len(data):
			break;
else:
	data = my_spn.data.train
	print len(my_spn.model.id_node_dict)
	a = 0
	ms = m_start
	n = m
	print ms
	for i in range(1+(len(data)-1)//ms):
		b = min(len(data), a + ms)
		if (a == b):
			break;
		n_data = data[a:b, :, 0:1]
		n_data = n_data[:, my_spn.input_order, :]
		n_data = np.reshape(n_data, (len(n_data), n_data.shape[1]*n_data.shape[2]))
		if i == n:
		 	my_spn.model.normalize_weights()
		if i > n:
			my_spn.model.apply_count(n_data, cf)
		if i < 9999:
			for j in range(r):
				print "yo"
		 		_, inpy, loss = my_spn.model.session.run([my_spn.model.opt_val, my_spn.model.computations[0], my_spn.model.loss], feed_dict = {my_spn.model.input: n_data})
                                print np.max(inpy)
                                print loss
		# else:
		# 	my_spn.model.session.run(my_spn.model.opt_val2, feed_dict = {my_spn.model.input: data[a:b]})
		a += ms
		if ms < minibatch_cap:
			ms *= factor
			ms = int(ms)
		if i % 10 == 110:
			print my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: myreshape(my_spn.data.test[0:500], my_spn)})
		print i
		if a > len(data):
			break;
end = time.time() - start;
print time.time()
print "total time: " + str(end)
total_loss = 0.0
for i in range(1+(len(my_spn.data.test)-1)//ms):
	b = min((i+1)*ms, len(my_spn.data.test))
	if a == b:
		break;
	test_loss = my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: myreshape(my_spn.data.test[i*ms:b], my_spn)})
	total_loss += test_loss*(float(b - i*ms))
test_loss = total_loss/float(len(my_spn.data.test))
total_loss = 0.0
'''
for i in range(len(my_spn.data.valid)//ms+1):
	b = min((i+1)*ms, len(my_spn.data.valid))
	valid_loss = my_spn.model.session.run(my_spn.model.loss, feed_dict={my_spn.model.input: myreshape(my_spn.data.valid[i*ms:b], my_spn)})
	total_loss += valid_loss*(float(b - i*ms))
	if b == len(my_spn.data.valid):
		break;
valid_loss = total_loss/float(len(my_spn.data.valid))
'''
print "Test Loss:"
print test_loss
print "Valid Loss:"
#print valid_loss
print "Test Loss:"
print test_loss
print "Valid Loss:"
#print valid_loss

myfile = open('mything/' + num  + mn + '.py', 'w')
myfile.write("losses = {'sbf': " + str(sbf) + "  'pbf': " + str(pbf)  +" 'size':" + str(my_size) +" 'layers':" + str(mylayers) +" 'test_loss':" + str(test_loss) + ", 'time_taken':" + str(end) + ", 'name': '"+ mn +"' }")
#for d in my_spn.data.valid.T[:100]:
	
#/float(len(my_spn.data.valid.T[:100]))
# my_spn2 = SPN()
# my_spn2.make_model_from_file('../spn_models/ + mn + .spn.txt', False)
# my_spn2.start_session()
# # print map(lambda x: x.get_shape(), my_spn2.model.weights)
# # print map(lambda x: len(x), my_spn2.model.node_layers)
# # print my_spn2.predict([[1]*len(my_spn2.input_order)*2])
# #my_spn2.make_model_from_file('../spn_models/ + mn + .spncc.spn.txt', True)
# # assert 1.1 >= my_spn2.predict([[1]]*1574)[0][0]
# my_spn2.add_data('../Data/ + mn + .ts.data')
# my_spn2.add_data('../Data/ + mn + .test.data', 'test')
# my_spn2.add_data('../Data/ + mn + .valid.data', 'valid')
# a = my_spn2.test(my_spn2.data.valid)
# print map(lambda x: np.sum(x), a)
# print map(lambda x: np.sum(x), b)
# print 'tests passed!'
