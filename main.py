from flask import Flask, render_template, url_for, session, request
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup

app=Flask(__name__)
Bootstrap(app)

District_URL = "https://en.wikipedia.org/wiki/List_of_districts_of_"
Data_URL = "https://en.wikipedia.org/wiki/"

@app.route('/', methods=["GET", "POST"])
def home_page():
    states=["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    return render_template("index.html", states=states)

@app.route('/district/', methods=["POST"])
def district():
    districts=[]
    state = request.form.get("statename")
    encr_state = (state.strip()).split(' ')
    url_state = '_'.join(encr_state)
    url = District_URL+url_state

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_dist = soup.find(name="table", class_="wikitable")
    all_dist = all_dist.select(selector="tbody tr td a")

    for dist in all_dist:
        try:
            d_title = dist.get("title")
            if (d_title.split(' '))[-1] == "district":
                districts.append(d_title.split(' district')[0])
        except:
            continue

    return render_template("district.html", districts=districts, state=state)

@app.route('/district/demography', methods=["POST"])
def demography():
    dst = request.form.get("districtname")
    encr_dst = (dst.strip()).split(' ')
    url_dst = '_'.join(encr_dst)
    url = Data_URL + url_dst + "_district"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    religions = soup.find(name="div", class_="barbox")
    religions = religions.select(selector="table tbody tr td")
    religion_lst = []

    for r in religions:
        try:
            d_title = r.getText()
            religion_lst.append(d_title)
        except:
            continue

    #REMOVING UNWANTED CHARS
    religion_lst[:] = (value for value in religion_lst if value != "\u2009")
    religion_lst[:] = (value for value in religion_lst if value != "")
    religion_lst = religion_lst[2:-1]

    #Converting to float
    for item in religion_lst:
        if item[-1]=="%":
            x=religion_lst.index(item)
            item = float(item[:-1])
            religion_lst[x] = item
        else:
            continue

    lcol = []
    rcol = []
    count = 1
    for i in religion_lst:
        if count%2!=0:
            lcol.append(i)
        else:
            rcol.append(i)
        count+=1

    lenlst = len(religion_lst)

    return render_template("data.html", dst=dst, lc = lcol, rc= rcol, rlst=religion_lst, lenlst=lenlst)


if __name__ == "__main__":
    app.run(debug=True)
