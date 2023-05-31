from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.data import Sentence
import numpy as np
import json

def sim(x, y):
    # Assuming X and Y are two vectors
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def get_years(year):
    year = int(year)
    if  (1970 <= year <= 1979):
        return 1970
    elif(1980 <= year <= 1989):
        return 1980 
    elif(1990 <= year <= 1999):
        return 1990 
    elif(2000 <= year <= 2009):
        return 2000 
    elif(2010 <= year <= 2019):
        return 2010 
    elif(2020 <= year <= 2029):
        return 2020
    return 0


# init embedding
# flair_embedding_forward = FlairEmbeddings('news-forward')

# category = ['effect', 'plot', 'character', 'genre', 'scene', 'actor', 'cast', 'sound', 'story', 'music', 'editing', 'picture', 'dialog', 'acting', 'visual', 'count']

# category_sentence = Sentence(category)
# flair_embedding_forward.embed(category_sentence)

# res = { 1970:{}, 1980:{}, 1990:{}, 2000:{}, 2010:{}, 2020:{}, 0:{}}

# for cat in category:
#     for year in res:
#         res[year][cat] = 0

# N = 250
# for i in range(1, N+1):
#     print(i)
#     data = json.loads(open(f"src/lda/Rank_{i}_lda.json", 'r').read())
    
#     for topic in data['topic']:
#         sentence = Sentence(topic)
#         flair_embedding_forward.embed(sentence)

#         for word in sentence:
#             word_emb = word.embedding
#             for cat in category_sentence:
#                 cat_emb = cat.embedding
#                 if(sim(word_emb, cat_emb) > 0.3):
#                     res[get_years(data['year'])][cat.text] += 1
#                     res[get_years(data['year'])]['count'] += 1


# for year in res:
#     print(year)
#     for cat in res[year]:
#         print(f"  {cat} {res[year][cat]}")

res = {}
res[1970] = {'effect':19, 'plot':134, 'character':294, 'genre': 712, 'scene': 785, 'actor':514, 'cast':1, 'sound':100, 'story':797, 'music':600, 'editing':645, 'picture':553, 'dialog':398, 'acting':206, 'visual':85, 'count':6517}
res[1980] = {'effect':52, 'plot':247, 'character':469, 'genre':1094, 'scene':1173, 'actor':795, 'cast':12, 'sound':156, 'story':1150, 'music':897, 'editing':937, 'picture':793, 'dialog':608, 'acting':348, 'visual':87, 'count':9798}
res[1990] = {'effect':61, 'plot':340, 'character':744, 'genre':1730, 'scene':1846, 'actor':1252, 'cast':19, 'sound':216, 'story':1880, 'music':1441, 'editing':1548, 'picture':1251, 'dialog':1023, 'acting':467, 'visual':149, 'count':15591}
res[2000] = {'effect':62, 'plot':483, 'character':920, 'genre':2024, 'scene':2073, 'actor':1421, 'cast':28, 'sound':274, 'story':2155, 'music':1650, 'editing':1751, 'picture':1420, 'dialog':1185, 'acting':564, 'visual':174, 'count':18124}
res[2010] = {'effect':70, 'plot':434, 'character':817, 'genre':1806, 'scene':1880, 'actor':1231, 'cast':28, 'sound':258, 'story':1921, 'music':1504, 'editing':1589, 'picture':1341, 'dialog':1042, 'acting':521, 'visual':174, 'count':16348}
res[2020] = {'effect':11, 'plot':70, 'character':146, 'genre':280, 'scene':285, 'actor':211, 'cast':7, 'sound':52, 'story':303, 'music':239, 'editing':251, 'picture':210, 'dialog':173, 'acting':92, 'visual':46, 'count':2654}
# res[0] = {'effect':59, 'plot':484, 'character':1097, 'genre':2866, 'scene':2977, 'actor':2047, 'cast':15, 'sound':340, 'story':3047, 'music':2244, 'editing':2454, 'picture':2096, 'dialog':1643, 'acting':763, 'visual':177, 'count':24975}


# make res into percentage
for year in res:
    for cat in res[year]:
        if(cat == 'count'):
            continue
        res[year][cat] = res[year][cat] / res[year]['count']

# make res into pendas table
import pandas as pd
df = pd.DataFrame(res)
print(df)

# # plot
# import matplotlib.pyplot as plt
# plt.legend()
# plt.plot([year for year in res], df.loc['effect'], label='effect')
# plt.show()

# plt.plot([year for year in res], df.loc['plot'], label='plot')
# plt.show()

# plt.plot([year for year in res], df.loc['character'], label='character')
# plt.show()

# plt.plot([year for year in res], df.loc['genre'], label='genre')
# plt.show()

# plt.plot([year for year in res], df.loc['scene'], label='scene')
# plt.show()


# plt.show()

