#the item that you want

import json
from pathlib import Path
from osrsbox import items_api
import bs4
import requests
from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen


# def removeSpace():

#Remove strings for URL 
def get_item(item_needed):
    new_itemString = ""
    for x in item_needed:
        if x == " ":
            new_itemString += "_"
        else:
            new_itemString += x
    return new_itemString


def parseProfit(item):
    space_removed = get_item(item)
    r = requests.get(f'https://oldschool.runescape.wiki/w/{space_removed}')
    soup = BeautifulSoup(r.content, 'html.parser')
    if soup.find(id = "Nothing_interesting_happens."):
        return f'The item "{item}" could not be found. Please enter another item.'
    item_name = soup.find(id = "firstHeading").get_text()
    get_tables = soup.findAll('table', class_ = 'wikitable align-center-1 align-right-3 align-right-4')[0]
    last_row1 = get_tables.findAll('tr')[-1].findAll('td')[0].findAll('span')[0].text
    
    if (len(item) > 4 and item [-5::] == "bolts"):
        fixed_amount = int(last_row1)/10
        return f'{item_name} is profitable, with a gain of {int(fixed_amount)}gp per item'
    if int(last_row1) < 0:
        return f'{item_name} is NOT profitable, with a loss of {last_row1}gp per item'
    else:
        return f'{item_name} is profitable, with a gain of {last_row1}gp per item'

def checkItemMarket():
    pass

def isItemTradeable():
    pass

# print(parseProfit("diamond dragon bolts"))
# fart  = "23123123123123 hoe!"
# print(fart[-4::])

def getPic():
    html =requests.get('https://oldschool.runescape.wiki/w/lobster')
    bs = BeautifulSoup(html.content, 'html.parser')
    images = bs.find_all('img', {'src': re.compile('.png')} )
    return images[0]['src']
    # return images1


print(getPic())