from os import system
from requests import get
from bs4 import BeautifulSoup
from orjson import loads
from json import loads

from lib.Globals import terms

def corona_news_launch():
    for _ in terms:
        _ = _.replace(' ', '+')
        system(f"firefox-esr 'https://www.google.com/search?client=firefox-b-e&q={_}'")

def fetch_pulls(url):
    response = BeautifulSoup(get(url).text, "html.parser")
    for resp in response.find_all("span", {"data-content": "Pull requests"}):
        for sibling in resp.next_siblings:
            if not sibling or sibling == '\n':
                continue
            open_pr =  f"{sibling['title']}"
    for resp in response.find_all("a", {"data-ga-click": "Pull Requests, Table state, Closed"}):
        if resp:
            closed = str(resp).split('</svg>\n')[-1].split('\n')[0].strip().split('Closed')[0]
            break
    return int(open_pr.replace(',', '')), int(closed.replace(',', ''))

def fetch_stars_subs(url):
    star = url + "stargazers"
    subs = url + "subscribers"
    star_r = get(star).text
    subs_r = get(subs).text
    star_load, subs_load = len(loads(star_r)), len(loads(subs_r))
    return star_load, subs_load

def fetch_corona_infection():
    response = BeautifulSoup(get("https://www.worldometers.info/coronavirus/").text, 'html.parser')
    r = list(list(response.find_all('tbody', {'class': 'total_row_body'})[0].children)[1].children)
    i, d = int(r[5].string.replace(',', '')), int(r[9].string.replace(',', ''))
    return i, d 
