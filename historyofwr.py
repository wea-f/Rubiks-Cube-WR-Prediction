from bs4 import BeautifulSoup
import requests
import pandas as pd

page = requests.get(
    "https://www.worldcubeassociation.org/results/records?event_id=333&show=history&years=all+years"
)

soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("tbody")
tableRows = table.find_all("tr")

data = []
for row in tableRows:
  if row.find(
      "td", class_="single"
  ) is not None:  # Rows beyond a point  switches to the 3x3 average world records instead of single
    time = row.find("td", class_="single").text
    name = row.find("td", class_="name").text
    date = row.find("td", class_="date").text

    data.append({"time": time, "name": name, "date": date})

df = pd.DataFrame.from_dict(data)
df.to_csv("wrhistory.csv", index=False)
