import spacy

from pathlib import Path
from pprint import pprint


class EntityRecogniser(object):

	def __init__(self, raw_text = None):
		self.raw_text = raw_text
		self.nlp = spacy.load('en_core_web_sm')

		if raw_text is not None:	
			self.doc = self.nlp(self.raw_text)
			self.doc_ent = self.doc.ents
		else:
			print("Text is not specified")
		self.entity_data = {}


	def get_entities(self):

		for item in self.doc_ent:
			entity = item.label_

			if entity:
				self.entity_data.update({
						'token' : item,
						'has_entity' : True,
						'entity' : entity,
						'start_position' : item.
					})



def main():
	e = EntityRecogniser("Hello, this is Mr. Frank.")
	e.get_entities()


if __name__ == "__main__":
	main()