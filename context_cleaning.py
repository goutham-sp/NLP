import re
import emoji_unicode


class CleanContext(object):

	def __init__(self):

		pass


	def __call__(self, content_to_clean):
		
		content = content_to_clean
		print()
		print()

		# Stupid Suhas fix this for words like dude, guys, etc.
		content = re.sub(r'\'[s]',' is',content)
		content = re.sub(r'\'[d]',' would',content)
		content = re.sub(r'[c]an\'[t]',' can not',content)
		content = re.sub(r'[w]on\'[t]',' will not',content)
		content = re.sub(r'[s]han\'[t]',' shall not',content)
		content = re.sub(r'[n]\'[t]',' not',content)
		content = re.sub(r'\'ve',' have',content)
		content = re.sub(r'\'re',' are',content)
		content = re.sub(r'\'ll',' will',content)
		content = re.sub(r'\'m',' am',content)
		content = re.sub(r'[\?]{2,}','?',content)
		content = re.sub(r'[\!]{2,}','!',content)
		content = re.sub(r'[:;](\-)?[\)\(pPDd]','',content)
		content = re.sub(r'(?<=[\s])\b[A-Za-z]\b(?=[\s])','',content)
		# content = self.replace_amp(content)
		content = content.replace(u'&', u'and')
		# content = re.sub(
		# 					u"^(\ud83d[\ude00-\ude4f])|"  # emoticons
		# 					u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
		# 					u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
		# 					u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
		# 					u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
		# 					u"+", '', content)
		
		# content = re.sub(r"[]", '', content)

		# content = ''.join(c for c in content if c <= '\uFFFF')

		content = self.remove_emoji(content)
		# content = self.remove_punctuations(content)
		
		content = re.sub(r'[?!.]+',".", content)
		print(content, "\n\n")

		return content


	def remove_emoji(self, content_to_clean):
		# content = re.compile()
		return emoji_unicode.replace(content_to_clean, lambda e: u''.format(filename=e.code_points, raw=e.unicode))


	def replace_amp(self, content):
		print(content)
		content = re.sub(r'[\&]+', 'and', content)
		return content


	def remove_slangs(self):

		# Write code here
		pass