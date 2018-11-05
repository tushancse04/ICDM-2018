from sklearn import svm
import pickle
import os
from config import config

class mln_generator(config):
	def __init__(self):
		config.__init__(self)

	def get_svm_weights(self,vectors,output_classes,vocab):
		pickle_location = self.pickle_location
		pickle_svm_file = self.pickle_svm_file
		if os.path.exists(pickle_svm_file):
			self.svm = pickle.load(open( pickle_svm_file, "rb" ) )
			return self.svm

		clf = svm.LinearSVC(C=1)

		clf.fit(vectors, output_classes)  
		print('fitting complete')
		coefs = []
		for x in clf.coef_:
			coefs.extend(x)
		min_val,max_val = min(coefs),max(coefs)
		coefs_matrix = []
		diff = max_val - min_val
		for i,x in enumerate(clf.coef_):
			coefs_matrix.append([])
			for y in x:
				coefs_matrix[i].append((y - min_val)/diff)



		for n in range(5):
			s = self.mini_batch_size
			if n == 4:
				s = 232
			mlnstr = ''
			for ptype in self.Page_Types:
				mlnstr += ptype + ':' + str(s) + ' '
			for w in vocab:
				mlnstr += 'HasWord_' + w + ':' + str(s) + ' '
			mlnstr += 'Linked:' + str(s) + ':' + str(s) + '\n'


			fname = 'test-' + str(n) + '.txt'
			ifile = open(self.db_location + fname)
			words = []
			for l in ifile:
				l = l.replace('!','').strip()
				if l.startswith('HasWord'):
					word = l.split('_')[1].split('(')[0]
					if word not in words:
						words.append(word)
			print(len(words))
			for i,t in enumerate(self.Page_Types):
				for j,w in enumerate(vocab):
					if w not in words:
						continue
					mlnstr += str(coefs_matrix[i][j]) + ':!HasWord_' + w + '(p) v !'  + t + '(p)\n'



			for i,t1 in enumerate(self.Page_Types):
				for j,t2 in enumerate(self.Page_Types):
					mlnstr += str(self.default_weight) + ':!Linked(p1,p2) v !' + t1 + '(p1) v !' + t2 + '(p2)\n' 

			ifile.close()
			ofile = open(self.mln_location + fname,'w')
			ofile.write(mlnstr)
			ofile.close()  