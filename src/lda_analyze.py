import gensim
from gensim import corpora
import json
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

# import nltk
# nltk.download('stopwords')


class lda_analyze:
    def __init__(self):
        pass

    def run(self):
        N = 250
        for i in range(1, N + 1):
            print(f"analyzing topic of rank_{i}")

            data = json.loads(open(f"data/Rank_{i}.json", "r").read())
            comments = []
            output_dict = {}
            output_dict["rank"] = data["rank"]
            output_dict["name"] = data["name"]
            output_dict["year"] = data["year"]
            output_dict["rating"] = data["rating"]
            output_dict["topic"] = [[] for i in range(10)]

            for j, review in enumerate(data["reviews"]):
                comments.append(review["content"])

            tokenizer = RegexpTokenizer(r"\w+")
            en_stop = stopwords.words("english")
            doc = []

            custom_stop_word = []
            # for word in ['i', 'movie', 'the', 's', 'film', 't', 'it', 'this', 'can', 'he', 'she', 'and', 'u']:
            #     custom_stop_word.append(word)
            #     custom_stop_word.append(word.capitalize())
            custom_stop_word.extend([i.lower() for i in data["name"].split()])
            custom_stop_word.extend([i.capitalize() for i in data["name"].split()])

            for comment in comments:
                doc.append(
                    [
                        i
                        for i in tokenizer.tokenize(comment)
                        if (i not in en_stop and i not in custom_stop_word)
                    ]
                )

            dic = corpora.Dictionary(doc)
            corpus = [dic.doc2bow(doc) for doc in doc]
            lda = gensim.models.LdaModel(
                corpus=corpus,
                id2word=dic,
                num_topics=10,
                random_state=100,
                update_every=1,
                passes=10,
                alpha="auto",
                per_word_topics=True,
            )

            for topic in lda.show_topics(formatted=False):
                for word, prob in topic[1]:
                    output_dict["topic"][topic[0]].append(word)
                    print(word, end=" ")
                print()

            with open(f"src/lda/Rank_{i}_lda.json", "w") as outfile:
                json.dump(output_dict, outfile)
    
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
        # years = [1990]
        output_dict = {'1990': {'topic':[[] for i in range(100)]}, 
                       '2000': {'topic':[[] for i in range(100)]}, 
                       '2010': {'topic':[[] for i in range(100)]}, 
                       '2020': {'topic':[[] for i in range(100)]}}
        for year in years:
            print(f"analyzing topic of year_{year}")
            comments = json.loads(open(f"src/lda/lda_comment_{year}.json", "r").read())
            tokenizer = RegexpTokenizer(r"\w+")
            en_stop = stopwords.words("english")
            doc = []
            # for comment in comments:
            #     doc.append(comment["comment"])
            #     # print(comment["comment"])

                
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
                num_topics=100,
                random_state=100,
                update_every=1,
                passes=10,
                alpha="auto",
                per_word_topics=True,
            )

            for topic in lda.show_topics(formatted=False):
                for word, prob in topic[1]:
                    output_dict[str(year)]['topic'][topic[0]].append(word)
                #     print(word, end=" ")
                # print()

        with open(f"src/lda/lda_comment_topic.json", "w") as outfile:
            json.dump(output_dict, outfile)
