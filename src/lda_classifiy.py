from flair.embeddings import WordEmbeddings
from flair.data import Sentence
from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer('stsb-roberta-large')
model = SentenceTransformer('stsb-mpnet-base-v2')

word = "school"
embedding = WordEmbeddings('en') # glove, en, crawl...
s = Sentence(word)
embedding.embed(s)
print(s[0].embedding) # first word in sentence