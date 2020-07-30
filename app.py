import requests, json

from flask import Flask, render_template as rnd
app = Flask(__name__)

def getTotal(headers):
    r = requests.get("https://www.vinbudin.is/addons/origo/module/ajaxwebservices/search.asmx/DoSearch?category=strong&skip=0&count=1&orderBy=random", headers=headers)
    response = r.json()['d']
    api = json.loads(response)
    total = api["total"]
    return total


#Getting API
headers = {"Content-Type": "application/json; charset=utf-8",}
r = requests.get(f"https://www.vinbudin.is/addons/origo/module/ajaxwebservices/search.asmx/DoSearch?category=strong&skip=0&count={getTotal(headers)}&orderBy=random", headers=headers)
response = r.json()['d']
api = json.loads(response)


alcPrice = []
info = []

x = api['data']

for i in range(len(api["data"])):
    price = x[i]['ProductPrice']
    vol = x[i]['ProductBottledVolume']
    alc = x[i]['ProductAlchoholVolume']

    alcPrice.append(price/(vol*0.01*alc))
    info.append([x[i]['ProductID'],x[i]['ProductName'],x[i]['ProductBottledVolume'],x[i]['ProductAlchoholVolume'],x[i]["ProductSubCategory"]["name"]])

id = info[alcPrice.index(min(alcPrice))][0]
name = info[alcPrice.index(min(alcPrice))][1]
ml = int(info[alcPrice.index(min(alcPrice))][2])
alc = info[alcPrice.index(min(alcPrice))][3]
cat = info[alcPrice.index(min(alcPrice))][4]

"""
print(f"Name:\t{name}")
print(f"Type:\t{cat}")
print(f"Vol:\t{ml} ml")
print(f"Alc:\t{alc}%")
print(f"ID:\t{id}")
"""

@app.route("/")
def index():
    return rnd("index.html", id=id, name=name, ml=ml, alc=alc, cat=cat)



if __name__ == "__main__":
    app.run(debug=True)