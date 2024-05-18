import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from bs4 import BeautifulSoup
import requests

# --------------------
# 1. Find the most qualified future 3x3 world record holder based on contendersParsedData
data = pd.read_csv("contendersParsedData.csv")


def calculate_score(row):
  return 100 + (0 - row["Fastest"] * 1.9) - (row["Slowest"] * 0.55) + (
      0 - row["Average"] * 2
  ) + (0 - row["Improvement"] * 1.2) - (row["Number of DNF's"] * 0.9) + (
      row["Number of 3x3 World Records"] * 0.15
  ) + (
      0 -
      row["Consistency"] *
      1.6
  )  # Multiplied by different values to weight them differently based on importance


df = pd.DataFrame(data)
df["Score"] = df.apply(calculate_score, axis=1)

# Get the cuber with the highest score
df = df.sort_values(by="Score", ascending=False)
best_cuber = df.iloc[0]

index = df[df["Cuber"] == best_cuber["Cuber"]].index[0]

df.drop([
    "Fastest", "Slowest", "Average", "Improvement", "Number of DNF's",
    "Number of 3x3 World Records", "Consistency"
],
        axis=1,
        inplace=True)
df.to_csv("contendersScoreLeaderboard.csv")

print("Predicted World record holder:" + str(best_cuber["Cuber"]))

# --------------
# 2. Get the best cuber's person record improvement rate.
# Get best cuber's id
page = requests.get(
    "https://www.worldcubeassociation.org/results/rankings/333/single?show=100+results"
)
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("tbody")
tableRows = table.find_all("tr")

candidates = []
for row in tableRows:
  name = row.find(class_="name")
  try:
    if str(best_cuber["Cuber"]) in name.text:
      id = name.find("a")["href"]
  except:
    pass

# Get cuber's profile based on id
page = requests.get("https://www.worldcubeassociation.org" + id)
soup = BeautifulSoup(page.content, "html.parser")

solvesTable = soup.find("tbody", class_="event-333")

personalRecords = []
count = 0
for r in solvesTable.find_all("tr"):
  if r.find("td", class_="competition") is not None and r.find(
      "td", class_="competition").text is not None:
    comp = r.find("td", class_="competition")
    if comp.find("a") is not None:
      compName = comp.find("a")
      compUrl = compName["href"]

  if r.find("td", class_="event") is None:  # correct row with records
    date = 0
    if r.find("td", class_="single pb") is not None:
      page = requests.get("https://www.worldcubeassociation.org" + compUrl)
      soup = BeautifulSoup(page.content, "html.parser")
      table = soup.find("div", class_="row competition-info")
      info = table.find("dl", class_="dl-horizontal compact")
      # Find Date
      for d in info.find_all("dd"):
        if d.find("a") is not None:
          try:
            date = pd.to_datetime(d.text)

          except:
            pass

      count += 1
      personalRecords.append({
          "Solve":
          r.find("td", class_="single pb").text.strip(),
          "Count":
          count,
          "Date":
          date
      })
    else:
      count += 1

  else:
    if r.find("td",
              class_="event").text.strip() != "3x3x3 Cube":  # 3x3 category
      break

df = pd.DataFrame.from_dict(personalRecords)

# ------------------------
# 3. Plotting the world record progression and best cuber's progression, finding the intersection between the two trend lines, the final prediction!
wrDf = pd.read_csv("wrhistory.csv")
cuberDf = pd.DataFrame.from_dict(personalRecords)

# Converting to correct format/data types
wrDf['date'] = pd.to_datetime(wrDf['date'])
cuberDf['Date'] = pd.to_datetime(cuberDf['Date'])

wrDf['time'] = pd.to_numeric(wrDf['time'])
cuberDf['Solve'] = pd.to_numeric(cuberDf['Solve'])


# Modified seaborn Regplot function to that also returns the slope and intercept
def regplot(*args, line_kws=None, marker=None, scatter_kws=None, **kwargs):
  # All of this is the same code
  plotter = sns.regression._RegressionPlotter(*args, **kwargs)

  ax = kwargs.get("ax", None)
  if ax is None:
    ax = plt.gca()

  scatter_kws = {} if scatter_kws is None else copy.copy(scatter_kws)
  scatter_kws["marker"] = marker
  line_kws = {} if line_kws is None else copy.copy(line_kws)

  plotter.plot(ax, scatter_kws, line_kws)

  # Modified code below to retrieve slope and intercept (taken from https://stackoverflow.com/questions/22852244/how-to-get-the-numerical-fitting-results-when-plotting-a-regression-in-seaborn)
  grid, yhat, err_bands = plotter.fit_regression(plt.gca())

  slope = (yhat[-1] - yhat[0]) / (grid[-1] - grid[0])
  intercept = yhat[0] - slope * grid[0]
  return slope, intercept


f, ax = plt.subplots()

# Convert timestamp format to float for regression
ax.xaxis.update_units(wrDf["date"])
ax.xaxis.update_units(cuberDf["Date"])

m1, b1 = regplot(x=ax.xaxis.convert_units(wrDf["date"]),
                 y=wrDf["time"],
                 label="World Record Trend")

m2, b2 = regplot(x=ax.xaxis.convert_units(cuberDf["Date"]),
                 y=cuberDf["Solve"],
                 label="Cuber personal records")

# Find intersection & and plot it
xi = (b1 - b2) / (m2 - m1)

dateNoWrTrend = (3.13 - b2) / m2  #3.13 is current world record
timeNoWrTrend = 3.12

yi = m1 * xi + b1  # slope intercept

ax.xaxis.update_units(xi)

# plt.axhline(y=wrDf['time'].min(), color='r', linestyle='--', label='Current World Record')

plt.axvline(x=ax.xaxis.convert_units(xi),
            color='green',
            linestyle='--',
            label="Intersection")
plt.axhline(y=yi, color='green', linestyle='--')

plt.plot(ax.xaxis.convert_units(xi),
         yi,
         marker="o",
         label="predicted record (intersection of orange and blue line)")

yi = round(yi, 2)
# Convert decimal year to date
decimalYear = (xi / 365) + 1970.025  # start date

decimalYearNoTrend = (dateNoWrTrend / 365) + 1970.025


def convert(decimalYear):
  year = int(decimalYear)
  remainder = decimalYear - year

  days_in_year = 365 if year % 4 != 0 or (year % 100 == 0
                                          and year % 400 != 0) else 366
  days = int(remainder * days_in_year)

  month_days = [
      31, 28 if days_in_year == 365 else 29, 31, 30, 31, 30, 31, 31, 30, 31,
      30, 31
  ]
  month = 1
  while days > month_days[month - 1]:
    days -= month_days[month - 1]
    month += 1

  date = str(year) + "-" + str(month) + "-" + str(days)
  return str(date)


print(
    str(best_cuber["Cuber"]) +
    " Will break the record. Predicted Record (intersection point): " +
    " Date: " + convert((xi / 365) + 1970.025) + " Solve time: " + str(yi))

print(
    "Predicted Date when Cuber breaks record (3.12) without world record trend influence: "
    + convert(decimalYearNoTrend))

plt.xlabel('Date')
plt.ylabel('Time (seconds)')
plt.title('World Records vs Cuber Personal Records')
plt.legend()
plt.show()

plt.axhline(y=wrDf['time'].min(),
            color='r',
            linestyle='--',
            label='Current World Record')
plt.plot(dateNoWrTrend,
         3.12,
         marker="o",
         label="intersection of red and orange line")

ax.xaxis.update_units(cuberDf["Date"])
m2, b2 = regplot(x=ax.xaxis.convert_units(cuberDf["Date"]),
                 y=cuberDf["Solve"],
                 label="Cuber personal records")

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Time (seconds)')
plt.title('Cuber vs Current World Record')
plt.legend()
plt.show()
