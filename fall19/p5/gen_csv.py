import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
import re

r = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_hurricanes")
page = BS(r.text, "html.parser")

def get_month(string):
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    if (str(string).isdigit()):
        return (("0" + str(string))[-2:])
    else:
        for i in range(0, 12):
            if (string.lower() == months[i]):
                return ("0" + str(i+1))[-2:]

rows = []
for t in page.find_all("table"):
    th = t.find("th")
    if th == None:
        continue
    if th.get_text().strip() != "Name":
        continue
    for tr in t.find_all("tr"):
        td = tr.find("td")
        if td == None:
            continue
        a = td.find("a")
        name = td.get_text().strip()
        length = len(name.split(" "))
        if a == None or name == "Unnamed" or name == "Name":
            continue
        url = a["href"]
        if not url.startswith("/wiki/"):
            continue
        rows.append({"name":name, "href":"https://en.wikipedia.org" + url})

pages = {}
for row in rows:
    if row["href"] in pages:
        continue
    r = requests.get(row["href"])
    pages[row["href"]] = BS(r.text, "html.parser")

rows2 = []
hrefs = set()
for row in rows:
    if row["href"] in hrefs:
        continue
    hrefs.add(row["href"])
    page = pages[row["href"]]
    fields = {}
    for tr in page.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        tds = [td.get_text().strip().lower() for td in tds]
        if len(tds) != 2:
            continue
        fields[tds[0]] = tds[1].strip().lower().replace(",", "")

    try:
        row["name"] = row["name"].strip('"')

        if not fields["damage"].startswith("$"):
            continue
        damage = fields["damage"].lstrip("$").split(" ")
        if damage[1] == "million":
            row["damage"] = str(damage[0] + "M")
        elif damage[1] == "billion":
            row["damage"] = str(damage[0] + "B")
        elif str(damage[0])[-3:] == "000":
            row["damage"] = str(damage[0])[:-3] + "K"
        else:
            row["damage"] = str(damage[0])

        row["deaths"] = int(fields["fatalities"].replace(u"\xa0", u" ").replace("–", " ").replace("none", "0").split(" ")[0])

        formed_data = fields["formed"].replace(chr(160), " ").split(" ")
        row["formed"] = get_month(formed_data[0]) + "/" + ("0" + str(int(formed_data[1])))[-2:] + "/" + formed_data[2][:4]

        dissipated_data = fields["dissipated"].replace(chr(160), " ").split(" ")
        row["dissipated"] = get_month(dissipated_data[0]) + "/" + ("0" + str(int(dissipated_data[1])))[-2:] + "/" + dissipated_data[2][:4]

        m = re.match(r'.*?(\d+) mph', fields["highest winds"])
        row["mph"] = int(m.group(1))

        if (row["name"] == "Florence"):
            if (row["damage"] == "200K"):
                row["name"] = "FLORENCE"
            elif (row["damage"] == "2.9M"):
                row["name"] = "florence"
                
        rows2.append(row)
    except:
        pass
for row1 in rows2:
    for row in rows2:
        if ((row1["name"] == row["name"]) and (row1["formed"] == row["formed"]) and (row1["dissipated"] == row["dissipated"]) and (row1["mph"] == row["mph"]) and (row1["damage"] == row["damage"]) and (row1["deaths"] == row["deaths"]) and (row1["href"] != row["href"])):
            rows2.remove(row)

df = pd.DataFrame(rows2)
df = df[["name", "formed", "dissipated", "mph", "damage", "deaths"]]
df.to_csv("hurricanes.csv", index=False)
print("Open 'hurricanes.csv' to find the extracted data")
