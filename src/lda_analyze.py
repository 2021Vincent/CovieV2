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


if __name__ == "__main__":
    lda_analyze = lda_analyze()
    lda_analyze.run()
