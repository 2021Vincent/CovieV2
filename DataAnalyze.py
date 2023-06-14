import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime 
from scipy.interpolate import make_interp_spline
import matplotlib.dates as dates
import numpy as np
# analyze data 
# 1. pulish year / rating
# 2. average comment rating / years
# 3. average comment rating / rating
# 4. average comment rating, nlp score(TODO) / years  

# 1. pulish year / rating
def plot_year_rating(json_data):
    df = pd.DataFrame(columns=['name', 'year', 'rating'])
    
    for i in range(250):
        data = json_data[i]
        df = pd.concat([df, pd.DataFrame({'name': [data['name']], 'year': [int(data['year'])], 'rating': [data['rating']]})])
    
    # group by every five years from 1921 to 2023
    x = []
    y = []
    for i in range(1921, 2023, 10):
        x.append(f'{i}-{i+9}')
        y.append(df[(df['year'] >= i) & (df['year'] <= i+9)]['rating'].mean())
    plt.plot(x, y, label = 'Rating all')
    plt.title("Release year / Rating")
    plt.xlabel('year')
    plt.ylabel('rating')
    plt.legend()
    plt.show()

def plot_top250_distribution(json_data):
    df = pd.DataFrame(columns=['name', 'year', 'rating'])
    for i in range(250):
        data = json_data[i]
        df = pd.concat([df, pd.DataFrame({'name': [data['name']], 'year': [int(data['year'])]})])
    df['year'].hist(bins=25)
    plt.title("Top 250 release year distribution")
    plt.xlabel('year')
    plt.ylabel('count')
    plt.show()

def plot_comment_rating_years(json_data):
    # 電影出版年份 / 平均評論分數
    df = pd.DataFrame(columns=['name', 'year', 'comment_rating'])
    for i in range(250):
        data = json_data[i]
        reviews  = data['reviews']
        reviews = [review for review in reviews if review['rating'] != 0]
        mean_rating  = sum([review['rating'] for review in reviews]) / len(reviews)
        df = pd.concat([df, pd.DataFrame({'name': [data['name']], 'year': [int(data['year'])], 'comment_rating': [mean_rating]})])
    x = []
    y = []
    for i in range(1921, 2023, 10):
        x.append(f'{i}-{i+9}')
        y.append(df[(df['year'] >= i) & (df['year'] <= i+9)]['comment_rating'].mean())
    plt.plot(x, y, label = 'Comment rating')
    plt.title("Release year / Average comment rating")
    plt.xlabel('year')
    plt.ylabel('comment_rating')
    # plt.show()
def plot_comment_rating_all_movie(json_data):
    # 畫出每部電影每年的平均分數
    year_rating = {}
    for i in range(250):
        data = json_data[i]
        reviews  = data['reviews']
        reviews = [review for review in reviews if review['rating'] != 0]
        for review in reviews:
            year_rating[int(review['date'][:4])] = year_rating.get(int(review['date'][:4]), []) + [review['rating']]
    x = []
    y = []
    for year in year_rating:
        x.append(year)
        y.append(sum(year_rating[year]) / len(year_rating[year]))
    plt.plot(x, y)
    plt.title("Comment year / Average comment rating")

    plt.xlabel('year')
    plt.ylabel('comment_rating')
    plt.show()
# 評論評分與純評分的關係
def plot_comment_rating(json_data):
    df = pd.DataFrame(columns=['name', 'year', 'rating', 'comment_rating'])
    for i in range(250):
        data = json_data[i]
        reviews  = data['reviews']
        reviews = [review for review in reviews if review['rating'] != 0]
        for review in reviews:
            df = pd.concat([df, pd.DataFrame({'name': [data['name']], 'year': [int(data['year'])], 'rating': [data['rating']], 'comment_rating': [review['rating']]})])
    df.plot.scatter(x='rating', y='comment_rating')
    plt.title("Rating / Comment rating")
    plt.xlabel('rating')
    plt.ylabel('comment_rating')
    plt.show()

if __name__ == '__main__':
    data = []
    for i in range(250):
        with open(f'data/Rank_{i+1}.json', 'r') as f:
            data.append(json.load(f))
    plot_top250_distribution(data)
    plot_comment_rating_years(data)
    plot_year_rating(data)
    plot_comment_rating_all_movie(data)