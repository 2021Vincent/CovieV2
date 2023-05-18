import requests
import bs4
import re
import json
import numpy as np
import pandas as pd
import datetime as dt
def crawl_imdb_comments(url):
    res = []
    review_url = url + "reviews" + "?sort=submissionDate&dir=asc&ratingFilter=0"
    soup = bs4.BeautifulSoup(requests.get(review_url, headers = {'accept-language':'en-US'}).text, "html.parser")
    # save html file
    with open(f"data/MovieData.html", mode="w+", encoding="utf8") as f:
        f.write(soup.prettify())
    review_list = soup.find_all("div", attrs = {'class' : 'lister-item-content'})
    comment_count = 0
    for review in review_list:
        assert review is not None
        comment_count += 1
        comment = {}
        comment["review"] = review.find("div", attrs = {'class' : 'text show-more__control'}).text
        rating = review.find("span", attrs = {'class' : 'rating-other-user-rating'})
        comment["rating"] = rating if rating is None else rating.find("span").text
        helpful = review.find("div", attrs = {'class' : 'actions text-muted'}).text.split()
        comment["helpful"] = helpful[0] if len(helpful) > 0 else 0
        comment["total"] = helpful[3] if len(helpful) > 3 else 0
        comment["title"] = review.find("a", attrs = {'class' : 'title'}).text
        comment["date"] = pd.to_datetime(review.find("span", attrs = {'class' : 'review-date'}).text)
        comment["url"] = "https://www.imdb.com" + review.find("a", attrs = {'class' : 'title'})["href"]
        res.append(comment)
    print(res[0])
    return res
def to_json(res):
    with open(f"data/MovieData.json", mode="w+", encoding="utf8") as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
if __name__ == '__main__':
    url = 'https://www.imdb.com/chart/top/'
    soup = bs4.BeautifulSoup(
        requests.get(url, headers = {'accept-language':'en-US'}).text, "html.parser")
    data = soup.find_all("tbody", attrs = {'class' : 'lister-list'})[0].find_all("tr")
    Top250 = []
    for i in range(250):
        res = {}
        res["rank"] = i+1
        res["name"] = data[i].find("td", attrs = {'class' : 'titleColumn'}).find("a").text
        res["url"] = "https://www.imdb.com" + data[i].find("td", attrs = {'class' : 'titleColumn'}).find("a")["href"]
        res["year"] = data[i].find("td", attrs = {'class' : 'titleColumn'}).find("span").text[1:-1]
        res["rating"] = float(data[i].find("td", attrs = {'class' : 'ratingColumn imdbRating'}).find("strong").text)
        res["rating count"] = int(data[i].find("td", attrs = {'class' : 'ratingColumn imdbRating'}).find("strong")["title"].split(' ')[3].replace(",", ""))
        res["comments"] =  crawl_imdb_comments(res["url"])
        Top250.append(res)
    # print(Top250)