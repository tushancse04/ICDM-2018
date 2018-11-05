class config():
	def __init__(self):
		self.page_class_file = 'db/page-classes.texas.db'
		self.page_word_file = 'db/page-words.texas.db'
		self.db_location = 'db/'
		self.pickle_location = 'pickle/'
		self.pickle_svm_file = self.pickle_location + 'svm.p'
		self.mini_batch_size = 50
		self.PTypes = ['Author']
		self.default_weight = 10.0
		self.mln_location  = 'mln/'
		