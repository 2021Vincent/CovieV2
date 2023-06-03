from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.data import Sentence
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json


class lda_classify:
    def __init__(self):
        self.res = {}
        self.category = [
            "effect",
            "plot",
            "character",
            "genre",
            "scene",
            "actor",
            "cast",
            "sound",
            "story",
            "music",
            "editing",
            "picture",
            "dialog",
            "acting",
            "visual",
            "cat_total",
            "topic_total",
        ]

    def sim(self, x, y):
        return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

    def get_years(year):
        year = int(year)
        if 1970 <= year <= 1979:
            return 1970
        elif 1980 <= year <= 1989:
            return 1980
        elif 1990 <= year <= 1999:
            return 1990
        elif 2000 <= year <= 2009:
            return 2000
        elif 2010 <= year <= 2019:
            return 2010
        elif 2020 <= year <= 2029:
            return 2020
        return 0

    def load_res(self):
        self.res = json.loads(open("src/lda/lda_classify_comment_result.json", "r").read())

    # def run(self):
    #     flair_embedding_forward = FlairEmbeddings("news-forward")
    #     category_sentence = Sentence(self.category)
    #     flair_embedding_forward.embed(category_sentence)

    #     res = {1970: {}, 1980: {}, 1990: {}, 2000: {}, 2010: {}, 2020: {}, 0: {}}
    #     for cat in self.category:
    #         for year in res:
    #             res[year][cat] = 0

    #     N = 250
    #     for i in range(1, N + 1):
    #         print(f"classfy topics from rank_{i}")
    #         data = json.loads(open(f"src/lda/Rank_{i}_lda.json", "r").read())

    #     for topic in data["topic"]:
    #         sentence = Sentence(topic)
    #         flair_embedding_forward.embed(sentence)

    #         topic_cat = []

    #         for word in sentence:
    #             word_emb = word.embedding
    #             for cat in category_sentence:
    #                 cat_emb = cat.embedding
    #                 if (cat.text not in topic_cat) and (self.sim(word_emb, cat_emb) > 0.3):
    #                     topic_cat.append(cat.text)
                
    #             for cat in topic_cat:
    #                 res[self.get_years(data["year"])][cat] += 1
    #                 res[self.get_years(data["year"])]["count"] += 1
    #             if topic_cat:
    #                 res[self.get_years(data["year"])]["per_topic"] += 1

    #     # save the result
    #     with open("src/lda/lda_classify_result.json", "w") as outfile:
    #         json.dump(res, outfile)
    #     self.res = res

    def show_res(self):
        df = pd.DataFrame(self.res)
        # df = df.drop('0', axis=1)
        print(df)


        # bar chart for every year
        the_category = ['genre', 'story', 'dialog', 'scene', 'character', 'actor', 'music']
        year_color = {'1990': "#81e1b3", '2000': "#87c4f2", '2010': "#8189ff", '2020': "#b362f9"}
        for year in df.head():
            df[year][the_category].plot.bar(color = year_color[year])
            plt.title(year)
            plt.show()


        # make res into percentage
        for year in df.head():
            for cat in self.res[year]:
                if cat == "topic_total" or cat == "cat_total":
                    continue
                df.loc[cat, year] /= df.loc["topic_total", year]
        print(df)


        # plot
        for cat in ['genre', 'story', 'dialog', 'scene', 'character', 'actor', 'music']:
            if cat == "topic_total" or cat == "cat_total":
                continue
            # limit the range of y axis
            plt.ylim(0, 1)
            df.loc[cat].plot(label=cat, marker = 'o')
            plt.title(cat)
            plt.show()
        # plt.legend()
        ["chararcter","genre","scene","actor","story","music","editing", "picture", "dialog", "acting"]

    def run_by_year(self):
        flair_embedding_forward = FlairEmbeddings("news-forward")
        category_sentence = Sentence([i for i in self.category if i != "cat_total" and i != "topic_total"])
        flair_embedding_forward.embed(category_sentence)

        res = {1990: {}, 2000: {}, 2010: {}, 2020: {}}
        for cat in self.category:
            for year in res:
                res[year][cat] = 0
        
        years = [1990, 2000, 2010, 2020]
        # years = [1990]
        TOPIC_NUM = 50
        # year_file_cnt = {1990: 1, 2000: 11, 2010: 13, 2020: 10}



        for year in years:
            # for file_cnt in range(1, year_file_cnt[year]+1):
            print(f"classfying topic of year_{year}")
            data = json.loads(open(f"src/lda/lda_comment_topic_{year}.json", "r").read())

            for topic in data[str(year)]['topic']:
                sentence = Sentence(topic)
                flair_embedding_forward.embed(sentence)

                topic_cat = []
                for word in sentence:
                    word_emb = word.embedding
                    for cat in category_sentence:
                        cat_emb = cat.embedding
                        if (cat.text not in topic_cat) and (self.sim(word_emb, cat_emb) > 0.45):
                            topic_cat.append(cat.text)
                        
                for cat in topic_cat:
                    res[year][cat] += 1
                    res[year]["cat_total"] += 1
                if topic_cat:
                    res[year]["topic_total"] += 1

        # save the result
        with open("src/lda/lda_classify_comment_result.json", "w") as outfile:
            json.dump(res, outfile)
                            
if __name__ == "__main__":
    lda_classify = lda_classify()
    # lda_classify.run_by_year()
    lda_classify.load_res()
    lda_classify.show_res()

'''
['genre', 'story', 'dialog', 'scene', 'character', 'actor', 'music']


[ girl,      possessed, Vincent,   knight, God, 
  encourage, Malcom,    possesses, kills,  Cole ]

[ Mr,     super,  Incredible, family, hero, 
  powers, heroes, Fantastic,  life,   Four ]


[ movie, This, film, It, I, one, Death, A, best, see ]
[ I, movie, see, time, one, It, seen, like, movies, This ]
'''