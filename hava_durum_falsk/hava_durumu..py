from flask import Flask,render_template,request
from bs4 import BeautifulSoup
import requests 
import time
app = Flask(__name__)

def hava_durumu(sehir):
    veri   = requests.get(f"https://havadurumu15gunluk.org/havadurumu/{sehir}-hava-durumu-15-gunluk.html")
    if veri.status_code == 200:
        veri = veri.content
        html_veri = BeautifulSoup(veri,"html.parser")

    gerekli = html_veri.find("div",{"class":"box__content"})

    durum = gerekli.find("span",{"class":"status"}).text
    derece = gerekli.find("span",{"class":"temp high bold"}).text
    derece = derece.split("°")
    derece = derece[0]
    hissedilen = gerekli.find("span",{"class":"temp low"}).text
    hissedilen = hissedilen.split("°")
    hissedilen = hissedilen[0]
    hissedilen = hissedilen.split(" ")
    hissedilen = hissedilen[1]
    y = gerekli.find("ul").find_all("li")
    t = 0
    for i in y:
        if(t == 1):
            m = i.find("span",{"class":"bold"})
            nem = m.text
            break
        t +=1
    return durum,derece,hissedilen,nem




@app.route("/")
def kontrol():
   return render_template("index.html")

@app.route("/",methods=["POST"])
def kontrol_post():
   şehir = request.form["sehir"]
   durum,derece,hissedilen,nem = hava_durumu(şehir)
   şehir  =şehir.capitalize()
   time.sleep(2)
   return render_template("index2.html",sehir_adi=şehir,derece=derece,konum=şehir,hissedilen=hissedilen,nem=nem,durum=durum)




if __name__=="__main__":
   app.run(debug=True)