from __future__ import unicode_literals, print_function

import random
from pathlib import Path
import spacy


# You need to define a mapping from your data's part-of-speech tag names to the
# Universal Part-of-Speech tag set, as spaCy includes an enum of these tags.
# See here for the Universal Tag Set:
# http://universaldependencies.github.io/docs/u/pos/index.html
# You may also specify morphological features for your tags, from the universal
# scheme.
"""
	Tag map structure
	{
		'N': {'pos': 'NOUN'},
		'V': {'pos': 'VERB'},
		'J': {'pos': 'ADJ'}
	}

	Train data stucture

	[
		("I like green eggs", {'tags': ['N', 'V', 'J', 'N']}),
		("Eat blue ham", {'tags': ['V', 'J', 'N']})
	]

"""


class POSTrainer(object):

	def __init__(self, TAG_MAP = None, TRAIN_DATA = None):

		"""
			Create a new model, set up the pipeline and train the tagger. In order to
			train the tagger with a custom tag map, we're creating a new Language
			instance with a custom vocab.

			params:
			....TAG_MAP = Tag map as specified in the structure
			....TRAIN_DATA = Training data for the POS Trainer as specified in structure
		"""
		self.TAG_MAP = TAG_MAP
		self.TRAIN_DATA = TRAIN_DATA


	def __call__(self, lang = "en", output_dir = None, n_iter = 25):
	
		"""
			params:
			....lang = ISO Code of language to use
			....output_dir = Optional output directory
			....n_iter = Number of training iterations

			returns:
			....None
		"""
		nlp = spacy.blank(lang)
		# add the tagger to the pipeline
		# nlp.create_pipe works for built-ins that are registered with spaCy
		tagger = nlp.create_pipe('tagger')
		# Add the tags. This needs to be done before you start training.
		for tag, values in self.TAG_MAP.items():
			tagger.add_label(tag, values)
		nlp.add_pipe(tagger)

		optimizer = nlp.begin_training()
		for i in range(n_iter):
			random.shuffle(self.TRAIN_DATA)
			losses = {}
			for text, annotations in self.TRAIN_DATA:
				nlp.update([text], [annotations], sgd=optimizer, losses=losses)
			print(losses)

		# test the trained model
		test_text = "I like blue eggs"
		doc = nlp(test_text)
		print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])

		# save model to output directory
		if output_dir is not None:
			output_dir = Path(output_dir)
			if not output_dir.exists():
				output_dir.mkdir()
			nlp.to_disk(output_dir)
			print("Saved model to", output_dir)

			# test the save model
			print("Loading from", output_dir)
			nlp2 = spacy.load(output_dir)
			doc = nlp2(test_text)
			print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])