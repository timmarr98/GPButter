from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Runescape Items
class Items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(70))
    profit = db.Column(db.Integer)
    isProfit = db.Column(db.Boolean)
    itemIcon = db.Column(db.String(150))
    # pic = db.Column(db.String(100))


@app.route('/')
def index():
    #show the items
    item_list = Items.query.all()
    print(item_list)
    return render_template('base.html', item_list = item_list)

@app.route("/add", methods = ["POST"])
def addItem():
    #adds the new item from the user
    title = request.form.get("title")
    profit_factor = parseProfit(title)
    itemIcon1 =  f'https://oldschool.runescape.wiki/{getPic(title)}'
    isProfitable = False
    if int(profit_factor) > 0:
        isProfitable = True
    else:
        isProfitable = False
    new_itemEntry = Items(item = title, profit = int(parseProfit(title)), isProfit = isProfitable, itemIcon = itemIcon1)
    db.session.add(new_itemEntry)
    db.session.commit()
    return redirect(url_for("index"))

#remove the item that you don't want to track
@app.route("/remove/<int:item_id>")
def remove(item_id):
    item = Items.query.filter_by(id= item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

# Removes the spaces
def get_item(item_needed):
    new_itemString = ""
    for x in item_needed:
        if x == " ":
            new_itemString += "_"
        else:
            new_itemString += x
    return new_itemString
# Removes the comma's in order to properly type cast the string 
# as an int
def takeComs(number):
    new_num = ""
    for x in str(number):
        if x == ",":
            new_num+= ""
        else:
            new_num+=x
    return new_num

def getPic(item):
    html =requests.get(f'https://oldschool.runescape.wiki/w/{get_item(item)}')
    bs = BeautifulSoup(html.content, 'html.parser')
    images = bs.find_all('img', {'src': re.compile('.png')} )
    if images[0]['src'] == "/images/3/30/Coins_10000.png?7fa38":
        return str(images[1]['src'])
    else:
        return str(images[0]['src'])

#Calculate the profit for the 
def parseProfit(item):
    space_removed = get_item(item)
    r = requests.get(f'https://oldschool.runescape.wiki/w/{space_removed}')
    soup = BeautifulSoup(r.content, 'html.parser')
    if soup.find(id = "Nothing_interesting_happens."):
        return f'The item "{item}" could not be found. Please enter another item.'
    item_name = soup.find(id = "firstHeading").get_text()
    get_tables = soup.findAll('table', class_ = 'wikitable align-center-1 align-right-3 align-right-4')[0]
    last_row1 = get_tables.findAll('tr')[-1].findAll('td')[0].findAll('span')[0].text
    
    if (len(item) > 4 and item [-5::] == "bolts" or item[-5::] == "arrow"):
        fixed_amount = int(takeComs(last_row1))/10
        return int(float(takeComs(fixed_amount)))
    if int(takeComs(last_row1)) < 0:
        return int(float(takeComs(last_row1)))
    else:
        return int(float(takeComs(last_row1)))

if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(debug=True)
