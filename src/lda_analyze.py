import gensim
from gensim import corpora
from pprint import pprint
import json
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


for i in range(1, 251):
    print(f"Rank_{i} is processing...")

    data = json.loads(open(f"data/Rank_{i}.json", 'r').read())

    comments_pos = []
    comments_neg = []
    comments = []

    output_dict = {}
    output_dict['rank'] = data['rank']
    output_dict['name'] = data['name']
    output_dict['year'] = data['year']
    output_dict['rating'] = data['rating']
    output_dict['topic'] = [[] for i in range(10)]
    # output_dict['topic_pos'] = [[] for i in range(10)]
    # output_dict['topic_neg'] = [[] for i in range(10)]

    for j, review in enumerate(data['reviews']):
        # if((review['rating'])>=7):
        #     comments_pos.append(review['content'])
        # if(1<= review['rating']<=3):
        #     comments_neg.append(review['content'])
        comments.append(review['content'])
    
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = stopwords.words("english")
    doc_pos = []
    doc_neg = []
    doc = []

    custom_stop_word = []
    # for word in ['i', 'movie', 'the', 's', 'film', 't', 'it', 'this', 'can', 'he', 'she', 'and', 'u']:
    #     custom_stop_word.append(word)
    #     custom_stop_word.append(word.capitalize())
    custom_stop_word.extend([i.lower() for i in data['name'].split()])
    custom_stop_word.extend([i.capitalize() for i in data['name'].split()])
    # for comment in comments_pos:
    #     doc_pos.append([i for i in tokenizer.tokenize(comment) if (i not in en_stop and i not in custom_stop_word)])
    # for comment in comments_neg:
    #     doc_neg.append([i for i in tokenizer.tokenize(comment) if (i not in en_stop and i not in custom_stop_word)])
    for comment in comments:
        doc.append([i for i in tokenizer.tokenize(comment) if (i not in en_stop and i not in custom_stop_word)])


    # dic_pos = corpora.Dictionary(doc_pos)
    # dic_neg = corpora.Dictionary(doc_neg)
    dic = corpora.Dictionary(doc)


    # corpus_pos = [dic_pos.doc2bow(doc) for doc in doc_pos]
    # corpus_neg = [dic_neg.doc2bow(doc) for doc in doc_neg]
    corpus = [dic.doc2bow(doc) for doc in doc]

    # lda_pos = gensim.models.LdaModel(corpus=corpus_pos, id2word=dic_pos, num_topics=10,
    #                                     random_state=100,
    #                                     update_every=1,
    #                                     passes=10,
    #                                     alpha='auto',
    #                                     per_word_topics=True)
    # lda_neg = gensim.models.LdaModel(corpus=corpus_neg, id2word=dic_neg,
    #                                     num_topics=10,
    #                                     random_state=100,
    #                                     update_every=1,
    #                                     passes=10,
    #                                     alpha='auto',
    #                                     per_word_topics=True)
    lda = gensim.models.LdaModel(corpus=corpus, id2word=dic,
                                        num_topics=10,
                                        random_state=100,
                                        update_every=1,
                                        passes=10,
                                        alpha='auto',
                                        per_word_topics=True)
    
    # for topic in lda_pos.show_topics(formatted=False):
    #     for word, prob in topic[1]:
    #         output_dict['topic_pos'][topic[0]].append(word)
    #         print(word, end=' ')
    #     print()
    # print()

    # for topic in lda_neg.show_topics(formatted=False):
    #     for word, prob in topic[1]:
    #         output_dict['topic_neg'][topic[0]].append(word)
    #         print(word, end=' ')
    #     print()
    # print()

    for topic in lda.show_topics(formatted=False):
        for word, prob in topic[1]:
            output_dict['topic'][topic[0]].append(word)
            print(word, end=' ')
        print()
    
    
    with open(f"src/lda/Rank_{i}_lda.json", 'w') as outfile:
        json.dump(output_dict, outfile)
