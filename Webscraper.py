
# coding: utf-8

# In[39]:


import requests
import pandas
from bs4 import BeautifulSoup

r = requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
#r = requests.get("https://www.century21.ca/search/Q-Toronto%2C%20ON/44.001512215059776;-80.10212799818999;43.41283331345756;-78.65055939467436/v_Hybrid")
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div", {"class": "propertyRow"}) #find all divs with the class of propertyRow

all[0].find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ","")


l = []
#Getting content from more than one page
base_url = "http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, 30, 10):
    print(base_url + str(page) + ".html")
    r = requests.get(base_url + str(page) + ".html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})
    for item in all:
        d={}
        d["Price"] = item.find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ","")
        d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
        try:
            d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        try:
            d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Area"] = item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Baths"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None

        try:
            d["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None
        for column_group in item.find_all("div", {"class", "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class", "featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text

        l.append(d)


df = pandas.DataFrame(l)
df.to_csv("Output123.csv") #makes a csv file into the main folder

    

