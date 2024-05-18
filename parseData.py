import pandas as pd
from sklearn.linear_model import LinearRegression 

df = pd.read_csv("contendersRecentSolves.csv")
wrCount = pd.read_csv("numOfRecords.csv")

contenderParsedData = []
for index, row in df.iterrows():
  row["Solves"] = [eval(i) for i in eval(row["Solves"])] # Convert solves from string to int

  # Fastest Solve
  fastestSolve = 100
  for solve in row["Solves"]:
    if solve != 0: # 0 = DNF (did not finish)
      if solve < fastestSolve:
        fastestSolve = solve
        
  # Slowest Solve  
  slowestSolve = max(row["Solves"]) 

  # Number of Did Not Finishes
  numOfDNF = 0
  for s in range(len(row["Solves"])):
    if row["Solves"][s] == 0:
      row["Solves"][s] = round(float(0.8 * slowestSolve), 2) # Make DNF an actual time 
      numOfDNF += 1
      
  # Average
  average = round(round(sum(row["Solves"]), 2)  / len(row["Solves"]), 2)

  # Improvement rate
  x = [[i] for i in range(len(row["Solves"]))]
  y = row["Solves"]

  model = LinearRegression()
  model.fit(x, y)

  improvement = model.coef_[0]

  # Consistency (standard deviation), the lower the better
  solvesDf = pd.DataFrame(row["Solves"])
  consistency = solvesDf.std(ddof = 0).to_string(index=False, dtype=False) # remove unecessary values

  # Number of 3x3 World Records
  numWr = wrCount["Number of 3x3 World Records"][index]
  
  contenderParsedData.append({
    "Cuber": row["Cuber"],
    "Fastest": fastestSolve,
    "Slowest": slowestSolve,
    "Average": average,
    "Improvement": round(float(improvement), 6),
    "Number of DNF's": numOfDNF,
    "Number of 3x3 World Records": numWr,
    "Consistency": round(float(consistency), 6)
  })

contenderParsedData = pd.DataFrame(contenderParsedData)
contenderParsedData.to_csv("contendersParsedData.csv", index=False)



  
    
