from __future__ import unicode_literals, print_function

import spacy
import random
from pathlib import Path
import os
from pprint import pprint

"""
	Sample format training data

	[('Who is Shaka Khan?', {
		'entities': [(7, 17, 'PERSON')]
	}),
	('I like London and Berlin.', {
		'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
	})]
"""
# training data
# self.TRAIN_DATA = [
# 	# Set training data
# ]


class EntityTrainer(object):
	"""
		Training class for the entity recognition

		params:
		....output_dir: Default value is current directory
						Directory of the trained model to be stored at
		....TRAINING_DATA: Default value is None
							Training Data for entitity recognizer
		....n_iter: Default value is 20
					Defines number of training iterations

		returns:
		....None
	"""

	def __init__(self, output_dir = None, TRAINING_DATA = None, n_iter = 20):
		
		self.output_dir = os.getcwd()
		if output_dir == None:
			pass
		else:
			self.output_dir = output_dir
		self.n_iter = n_iter
		self.TRAIN_DATA = TRAINING_DATA


	def train_with_new_model(self, model=None, new_model_name='other'):
		"""
			Call when the training needs to be done with new entities and new model name

			params:
			....model : default value None
						Model on which the training should happen
			....new_model_name : default value 'other'
						Model name on which the training data should be stored

			returns:
			....None
		"""
		"""Set up the pipeline and entity recognizer, and train the new entity."""
		
		if model is not None:
			nlp = spacy.load(model)  # load existing spaCy model
			print("Loaded model '%s'" % model)
		else:
			nlp = spacy.blank('en')  # create blank Language class
			print("Created blank 'en' model")

		# Add entity recognizer to model if it's not in the pipeline
		# nlp.create_pipe works for built-ins that are registered with spaCy
		if 'ner' not in nlp.pipe_names:
			ner = nlp.create_pipe('ner')
			nlp.add_pipe(ner)
		# otherwise, get it, so we can add labels to it
		else:
			ner = nlp.get_pipe('ner')

		ner.add_label(LABEL)   # add new entity label to entity recognizer

		# get names of other pipes to disable them during training
		other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
		with nlp.disable_pipes(*other_pipes):  # only train NER
			optimizer = nlp.begin_training()
			for itn in range(self.n_iter):
				random.shuffle(self.TRAIN_DATA)
				losses = {}
				for text, annotations in self.TRAIN_DATA:
					nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
							   losses=losses)
				print(losses)

		# test the trained model
		test_text = 'Do you like horses?'
		doc = nlp(test_text)
		print("Entities in '%s'" % test_text)
		for ent in doc.ents:
			print(ent.label_, ent.text)

		# save model to output directory
		if self.output_dir is not None:
			output_dir = Path(self.output_dir)
			if not output_dir.exists():
				output_dir.mkdir()
			nlp.meta['name'] = new_model_name
			nlp.to_disk(output_dir)
			print("Saved model to", output_dir)

			# test the saved model
			print("Loading from", output_dir)
			nlp2 = spacy.load(output_dir)
			doc2 = nlp2(test_text)
			for ent in doc2.ents:
				print(ent.label_, ent.text)


	def train_with_existing_entities(self, model=None):
		"""
			Call when the training needs to be done with existing entities

			params:
			....model : default value None
						Model on which the training should happen

			returns:
			....None
		"""
		if model is not None:
			nlp = spacy.load(model)  # load existing spaCy model
			print("Loaded model '%s'" % model)
		else:
			nlp = spacy.blank('en')  # create blank Language class
			print("Created blank 'en' model")

		# create the built-in pipeline components and add them to the pipeline
		# nlp.create_pipe works for built-ins that are registered with spaCy
		if 'ner' not in nlp.pipe_names:
			ner = nlp.create_pipe('ner')
			nlp.add_pipe(ner, last=True)
		# otherwise, get it so we can add labels
		else:
			ner = nlp.get_pipe('ner')

		# add labels
		for _, annotations in self.TRAIN_DATA:
			for ent in annotations.get('entities'):
				ner.add_label(ent[2])

		# get names of other pipes to disable them during training
		other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
		with nlp.disable_pipes(*other_pipes):  # only train NER
			optimizer = nlp.begin_training()
			for itn in range(self.n_iter):
				random.shuffle(self.TRAIN_DATA)
				losses = {}
				for text, annotations in self.TRAIN_DATA:
					nlp.update(
						[text],  # batch of texts
						[annotations],  # batch of annotations
						drop=0.5,  # dropout - make it harder to memorise data
						sgd=optimizer,  # callable to update weights
						losses=losses)
				print(losses)

		# test the trained model
		for text, _ in self.TRAIN_DATA:
			doc = nlp(text)
			print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
			print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

		# save model to output directory
		if self.output_dir is not None:
			output_dir = Path(self.output_dir)
			if not output_dir.exists():
				output_dir.mkdir()
			nlp.to_disk(output_dir)
			print("Saved model to", output_dir)

			# test the saved model
			print("Loading from", output_dir)
			nlp2 = spacy.load(output_dir)
			for text, _ in self.TRAIN_DATA:
				doc = nlp2(text)
				print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
				print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])