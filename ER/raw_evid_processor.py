from sklearn.feature_extraction.text import TfidfVectorizer
from mln_generator import mln_generator
from config import config
import sys

class raw_evid_processor(config):
	def __init__(self):
		config.__init__(self)


	def get_svm_features(self,pname,idx_origname_map,word_map,evid_map):
		corpus = {}
		l = len(idx_origname_map[pname])
		print('making pairs')
		for id1 in idx_origname_map[pname]:
			for id2 in idx_origname_map[pname]:
				words1,words2 = word_map[id1],word_map[id2]
				doc = ''
				for w1 in words1:
					for w2 in words2:
						doc += str(w1) + '_' + str(w2) + ' '
				id = str(id1) + '_' + str(id2)
				corpus[id] = doc


		docs = []
		author_pairs = []
		for d in corpus:
			docs.append(corpus[d])
			author_pairs.append(d)
		
		print('vectorizing...')

		vectorizer = TfidfVectorizer(min_df=1)
		vectorizer.fit(docs)
		vectors = []
		output_classes = []
		ap =[]
		for i,doc in enumerate(docs):
			p = author_pairs[i]
			ids = p.split('_')
			id1 = int(ids[0])
			id2 = int(ids[1])
			if [id1,id2] in evid_map['Same'+pname] or [id2,id1] in evid_map['Same'+pname]:
				output_classes.append(1)
				v = vectorizer.transform([doc]).toarray()
				vectors.append(v[0])
				ap.append([id1,id2])
			else:
				n = len([x for x in output_classes if x == 1])
				if n*2 > len(output_classes):
					output_classes.append(0)
					v = vectorizer.transform([doc]).toarray()
					vectors.append(v[0])
					ap.append([id1,id2])

		print('vectization complete')
		vocab = []
		for w in vectorizer.vocabulary_:
			vocab.append(w)
		return vectors,output_classes,vocab

	def process(self,filename):
		ifile = open(filename)
		evid_map = {}
		origname_idx_map = {}
		idx_origname_map = {}
		for l in ifile:
			l = l.strip()
			if len(l) == 0:
				continue
			parts = l.split('::')
			pname = parts[0].strip()
			if pname not in evid_map:
				evid_map[pname] = []
			parts = parts[1].split(',')
			vals = []
			for p in parts:
				inn_pname = p.split('_')[0]
				if inn_pname not in origname_idx_map:
					origname_idx_map[inn_pname] = {}
					idx_origname_map[inn_pname] = {}
				if p not in origname_idx_map[inn_pname]:
					l = len(origname_idx_map[inn_pname])
					origname_idx_map[inn_pname][p] =  l
					idx_origname_map[inn_pname][l] =  p
				vals.append(origname_idx_map[inn_pname][p])
			evid_map[pname].append(vals)

		word_map = {}
		for p in self.PTypes:
			if p not in word_map:
				word_map[p] = {}
			for vals in evid_map['HasWord' + p]:
				author_id = vals[0]
				word_id = vals[1]
				if author_id not in word_map[p]:
					word_map[p][author_id] = []
				word_map[p][author_id].append(word_id)

		print('word mapping done')


		ofile = open('db/evid.txt','w')
		for p in self.PTypes:
			pname = 'HasWord' + p
			for atom in evid_map[pname]:
				pid = atom[0]
				w = atom[1]
				l = pname + '_' + str(w) + '(' + str(pid) + ')\n'
				ofile.write(l)
		ofile.close()

		vectors = {}
		output_classes = {}
		vocab = {}
		for p in self.PTypes:
			print('feature generating for ' + p)
			vectors[p],output_classes[p],vocab[p] = self.get_svm_features(p,idx_origname_map,word_map[p],evid_map)
		mg = mln_generator()
		mg.create_mln(vectors,output_classes,vocab,idx_origname_map)
		return vectors


