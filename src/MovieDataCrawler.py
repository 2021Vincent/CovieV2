import requests
import bs4
import json
import time

DOCKER_ENABLED = True

def crawl_imdb_comments(url, movie_name=None):
    res = []
    if DOCKER_ENABLED:
        api = "http://172.24.211.179:3000"
    else:
        api = 'https://imdb-api.projects.thetuhin.com'
    id = url.split('/')[-2]
    api_url = api+'/reviews/' + id + '?option=date&sortOrder=desc'
    next_api = "🌐"
    while next_api != 'null':
        req = requests.get(api_url).json()
        next_api = req['next_api_path']
        review_list = req['reviews']
        for review in review_list:
            assert review is not None
            comment = {}
            comment["content"] = review['content']
            comment["rating"] = review['stars']
            comment['helpfulness'] = {}
            comment['helpfulness']["votedAsHelpful"] = review['helpfulNess']["votedAsHelpful"]
            comment['helpfulness']["votes"] = review['helpfulNess']["votes"]
            comment["heading"] = review['heading']
            comment["date"] = review['date']
            comment["url"] = review['reviewLink']
            res.append(comment)
        print(f'already crawl: {len(res)} reviews for {movie_name}')
        if next_api == None:
            break
        api_url = api + next_api
        if not DOCKER_ENABLED:
            time.sleep(1)
    return res


if __name__ == '__main__':
    url = 'https://www.imdb.com/chart/top/'
    soup = bs4.BeautifulSoup(
        requests.get(url, headers={'accept-language': 'en-US'}).text, "html.parser")
    data = soup.find_all("tbody", attrs={'class': 'lister-list'})[0].find_all("tr")
    for i in range(250):
        res = {}
        res["rank"] = i+1
        res["name"] = data[i].find("td", attrs={'class': 'titleColumn'}).find("a").text
        res["url"] = "https://www.imdb.com" + data[i].find("td", attrs={'class': 'titleColumn'}).find("a")["href"]
        res["year"] = data[i].find("td", attrs={'class': 'titleColumn'}).find("span").text[1:-1]
        res["rating"] = float(data[i].find("td", attrs={'class': 'ratingColumn imdbRating'}).find("strong").text)
        res["rating count"] = int(data[i].find("td", attrs={'class': 'ratingColumn imdbRating'}).find("strong")["title"].split(' ')[3].replace(",", ""))
        res["reviews"] = crawl_imdb_comments(res["url"], res["name"])
        with open(f'data/Rank_{i+1}.json', 'w') as f:
            json.dump(res, f)
