import pandas as pd
from bs4 import BeautifulSoup
import requests

# Step 1: Find all the contenders to the wr
# How: By getting the top 100 fastest solves in the world, and get the cuber and their ID
page = requests.get(
    "https://www.worldcubeassociation.org/results/rankings/333/single?show=100+results"
)
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("tbody")
tableRows = table.find_all("tr")

candidates = []
for row in tableRows:
  name = row.find(class_="name")
  id = name.find("a")["href"]

  candidates.append([name.text, id])

# Removing cubers who have appeared multiple times:
uniqueCubers = set()
cleanedCandidates = []

for cuber in candidates:
  if cuber[0] not in uniqueCubers:
    uniqueCubers.add(cuber[0])
    cleanedCandidates.append(cuber)

candidates = cleanedCandidates
print("World Record Contenders: ", candidates)

# Step 2: Get the solve data for each contender
# How: Access each cuber's solve history based on their ID, and get their last 50 solves.
contendersData = []
for contender in candidates:
  # Access their profile
  page = requests.get("https://www.worldcubeassociation.org" + contender[1])
  soup = BeautifulSoup(page.content, "html.parser")

  solvesTable = soup.find("tbody", class_="event-333")

  solves = []
  count = 0
  for row in solvesTable.find_all("tr"):
    data = row.find_all("td")
    # get latest solve data
    if len(data) > 1:
      solves.extend([
          data[7].text, data[8].text, data[9].text, data[10].text,
          data[11].text
      ])
      count += 5

      if count >= 50:  # (last 50 solves)
        # DNF (Did not finish), set as 0 instead.
        for s in range(len(solves)):
          if solves[s] == "DNF":
            solves[s] = "0"

        contendersData.append({"Cuber": contender[0], "Solves": solves})
        break

df = pd.DataFrame.from_dict(contendersData)
df.to_csv("contendersRecentSolves.csv", index=False)

# Step 2b: Find the number of 3x3 world records each contender has
# How: Access their profile like in step 2, but get the number of 3x3 world records they have (including 3x3 average too).
worldRecords = []
for contender in candidates:
  page = requests.get("https://www.worldcubeassociation.org" + contender[1] +
                      "?tab=records")

  soup = BeautifulSoup(page.content, "html.parser")

  count = 0
  recordTable = soup.find_all("table", class_="table table-striped")
  try:
    world = soup.find("div", class_="records")
    if world is not None:
      recordRange = world.find("h3", "text-center")
      if recordRange.text.strip() == "History of World Records":
        for r in recordTable[4].find_all("tr"):
          if r.find("td", class_="event") is None:  # correct row with records
            if r.find("td", class_="single") is not None or r.find(
                "td", class_="average") is not None:
              count += 1

          else:  # wrong row with event label instead
            if r.find("td", class_="event").text.strip() != "3x3x3 Cube":
              break
      else:
        count = 0

  except IndexError:  # No 3x3x3 records
    count = 0

  worldRecords.append({
      "Cuber": contender[0],
      "Number of 3x3 World Records": count
  })

df = pd.DataFrame.from_dict(worldRecords)
df.to_csv("numOfRecords.csv", index=False)
