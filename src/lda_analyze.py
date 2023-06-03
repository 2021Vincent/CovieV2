import gensim
from gensim import corpora
import json
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np

# import nltk
# nltk.download('stopwords')
class lda_analyze:
    def __init__(self):
        pass
    
    def combine_date_of_comment(self):
        N = 250
        
        res = {}
        for i in range(1, N + 1):
            data = json.loads(open(f"data/Rank_{i}.json", "r").read())
            for comment in data["reviews"]:
                comment_data = {}
                comment_data["rank"] = data["rank"]
                comment_data["name"] = data["name"]
                comment_data["movie_year"] = data["year"]
                comment_data["comment_year"] = eval(comment["date"].split("-")[0]) - eval(comment["date"].split("-")[0])%10
                comment_data["comment"] = comment["content"]
                if comment_data["comment_year"] not in res:
                    res[comment_data["comment_year"]] = []
                res[comment_data["comment_year"]].append(comment_data)
        
        for year in res:
            file_cnt = 1
            last_pos = 0
            for i in range(10000, len(res[year]), 10000):
                with open(f"src/lda/lda_comment_{year}_{file_cnt}.json", "w") as outfile:
                    json.dump(res[year][last_pos:i], outfile)
                last_pos = i
                file_cnt += 1
            with open(f"src/lda/lda_comment_{year}_{file_cnt}.json", "w") as outfile:
                json.dump(res[year][last_pos:], outfile)
    
    def analyze_year_comment(self):
        years = [1990, 2000, 2010, 2020]
        TOPIC_NUM = 50
        year_file_cnt = {1990: 2, 2000: 11, 2010: 13, 2020: 10}
        for year in years:
            # print(f"analyzing topic of year_{year}")
            output_dict = {}
            output_dict[str(year)] = {'topic_num':TOPIC_NUM*year_file_cnt[year], 'topic':[]}
            tokenizer = RegexpTokenizer(r"\w+")
            en_stop = stopwords.words("english")
            
            for file_cnt in range(1, year_file_cnt[year] + 1):
                print(f"analyzing topic of year_{year}_{file_cnt}")
                comments = json.loads(open(f"src/lda/lda_comment_{year}_{file_cnt}.json", "r").read())
            
                doc = []
                for comment in comments:
                    custom_stop_word = []
                    custom_stop_word.extend([i.lower() for i in comment["name"].split()])
                    custom_stop_word.extend([i.capitalize() for i in comment["name"].split()])
                    doc.append(
                        [ i
                            for i in tokenizer.tokenize(comment['comment'])
                            if (i not in en_stop and i not in custom_stop_word)
                        ]
                    )

                dic = corpora.Dictionary(doc)
                corpus = [dic.doc2bow(doc) for doc in doc]
                lda = gensim.models.LdaModel(
                    corpus=corpus,
                    id2word=dic,
                    num_topics=TOPIC_NUM*2,
                    random_state=100,
                    update_every=1,
                    passes=10,
                    per_word_topics=True
                )

            # print(lda.show_topics(formatted=False))
                for topic in lda.show_topics(num_topics = 50, formatted=False):
                    output_dict[str(year)]['topic'].append([])
                    for word, prob in topic[1]:
                        # output_dict[str(year)]['topic'][topic[0]].append([word, float(prob)])
                        output_dict[str(year)]['topic'][-1].append(word)
                #     print(word, end=" ")
                # print()

            with open(f"data/lda/lda_comment_topic_{year}.json", "w") as outfile:
                json.dump(output_dict, outfile)


if(__name__ == "__main__"):
    lda_analyze().analyze_year_comment()
