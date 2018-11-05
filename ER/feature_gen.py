from config import config

from sklearn.feature_extraction.text import TfidfVectorizer
from mln_generator import mln_generator



class feature_gen(config):

	def __init__(self):
		config.__init__(self)

	def get_page_type_idx(self,page_type):
		if page_type == 'Course':
			return 0
		if page_type == 'Person':
			return 1
		return 2

	def generate_features(self):
		page_idx_map = {}
		idx_page_map = {}
		pageidx_word_map = {}
		word_pageidx_map = {}
		pageidx_type_map = {}


		ifile = open(self.page_class_file)
		c = 0
		for l in ifile:
			parts = l.split('(')
			page_type = parts[0]
			page_url = parts[1].split(')')[0]
			if page_url not in page_idx_map:
				page_idx_map[page_url] = c
				idx_page_map[c] = page_url
				page_type_idx = self.get_page_type_idx(page_type)
				pageidx_type_map[c] = page_type_idx
				c += 1
		ifile.close()
		self.page_idx_map = page_idx_map
		self.idx_page_map = idx_page_map


		ifile = open(self.page_word_file)
		for l in ifile:
			parts = l.split('(')[1].split(')')[0].split(',')
			word = parts[0].strip()
			l = len(word)
			word = word[1:l-1]
			page_url = parts[1].strip()

			if page_url not in page_idx_map:
				continue
			page_idx = page_idx_map[page_url]
			if page_idx not in pageidx_word_map:
				pageidx_word_map[page_idx] = []
			pageidx_word_map[page_idx] += [word]

			if word not in word_pageidx_map:
				word_pageidx_map[word] = []
			word_pageidx_map[word] += [page_idx]
		ifile.close()

		input_words = []
		output_classes = []
		corpus = []
		pageidx_corpus_list = []
		for pageidx in pageidx_word_map:
			doc = ''
			for w in pageidx_word_map[pageidx]:
				doc += w + ' '
			corpus += [doc]
			pageidx_corpus_list += [pageidx]
			output_classes += [pageidx_type_map[pageidx]]
		vectorizer = TfidfVectorizer(min_df=1)
		vectorizer.fit(corpus)
		vectors = []
		for doc in corpus:
			v = vectorizer.transform([doc]).toarray()
			vectors.append(v[0])
		c = 0
		vocab = []
		for w in vectorizer.vocabulary_:
			vocab.append(w)

		mg = mln_generator()
		mg.get_svm_weights(vectors,output_classes,vocab)
		return vectors