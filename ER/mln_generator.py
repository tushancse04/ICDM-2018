from sklearn import svm
import pickle
import os
from config import config

class mln_generator(config):
	def __init__(self):
		config.__init__(self)

	def create_mln(self,vectors,output_classes,vocab,idx_origname_map):
		mln_header = ''
		middle_mln_portion = ''
		for p in vectors:
			mp = ''
			clf = svm.LinearSVC(C=1)

			clf.fit(vectors[p], output_classes[p])  

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

			l = str(len(idx_origname_map[p]))
			mln_header += 'Same' + p + ':' + l + ':' + l + ' '
 

			domain_added = {}
			for j,v in enumerate(coefs_matrix[0]):
				words = vocab[p][j].split('_')
				w1,w2 = words[0],words[1]
				if w1 not in domain_added:
					mln_header += 'HasWord' + p + '_' + str(w1) + ':' + str(len(idx_origname_map[p])) + ' '
					domain_added[w1] = None
				if w2 not in domain_added:
					mln_header  += 'HasWord' + p + '_' + str(w2) + ':' + str(len(idx_origname_map[p])) + ' '
					domain_added[w2] = None

				mp += str(v) + ':!HasWord' + p + '_' + str(w1) + '(a1) v !HasWord' + p + '_' + str(w2) + '(a2) v !Same' + p + '(a1,a2)\n'
			print(mp)
			middle_mln_portion += mp


		mln_footer = '10:!SameAuthor(a1,a2) v !SameAuthor(a2,a3) v SameAuthor(a1,a3)\n'
		mln_footer += '10:!SameTitle(t1,t2) v !SameTitle(t2,t3) v SameTitle(t1,t3)\n'
		mln_footer += '10:!SameVenue(v1,v2) v !SameVenue(v2,v3) v SameVenue(v1,v3)'
		mlnstr = mln_header + middle_mln_portion + mln_footer
		ofile = open(self.mln_location + 'mln.txt','w')
		ofile.write(mlnstr)
		ofile.close()
