# Rubix Cube WR Prediction
# Goal: Predict the next rubix cube 3x3 world record - <br> I will be finding the solve time, date, and cuber <br> 
**I will be doing this by:** <br>
+ By web scraping data from websites
  > Web scraping: Access a website's source code, then extracting specific data from tables in the website. I will be used the modules Beautiful Soup and requests to do this
+ Parsing (Examine or break down) cuber's data
+ Using linear regression to visualize the trend
<br>
**I will be doing this by finding the most qualified cuber, then visualize their improvement and compare it with the world record trend, and get the intersection between the two trend lines.**
   <br>

## Procedure: <br>
### To find the next world record holder:
1. #### Get World record contenders, and their data.
   > ##### Contenders will be from the top 100 3x3 fastest solves from the worldcubeassociation.org website, and I will get the cuber who did those solves.
2. #### Parse their recent data (last 50 solves)
  ##### The 7 variables to determine world record holder: <br>
> ##### Their trend/improvement (slope) <br>
> ##### Their best/worst  solve <br>
> ##### Consistency (standard deviation) <br>
> ##### Average <br>
> ##### Number of DNF's they had. DNF means "did not finish" <br>
> ##### Number of 3x3 world records that they already have <br>

3. #### Find the most qualified cuber based on those 7 variables. 
> In finalpredict.py, you can find a calculate_score function where you can edit the different weights (multipliers) to these variables that I orginally put for your own prediction!

4. #### Visualize the most qualified cuber's PR (personal record) improvement with a trend line. <br>

5. #### Compare the trend with the world record trend. To get world record progression, graph the history of 3x3 world records and find line of best fit. <br> 

6. #### Lastly, get the intersection of both to find the predicted date and time.

## Code Map:
+ historyofwr.py - Gets the world record history. It outputs the data into wrhistory.csv <br>
+ getCandidateData.py - Gets all of the contenders to the world record, then gets the latest 50 solves for data, and also gets the number of 3x3 world records each contenders has. It outputs the numOfRecords.csv and the contendersRecentSolves.csv <br>
+ parseData.py - Uses data, contendersRecentSolves.csv and numOfRecords.csv and finds the 7 variables for each contender and outputs all of the results into the contendersParsedData.csv <br>
+ finalpredict - First, it calculates the score based on the data from contendersParsedData.csv. It gets the cuber of best score. After that it gets the best cuber's improvement rate and graphs it. It graphs the world record progression too, and finds the intersection of the points. <br>
+ All of the csv files are results of/made from the python files, feel free to look at them to see the data that I used!

## Final Result (Code last ran on 4/21/24) : Xuanyi Geng will break the world record. A time of -1.27 and on December 1st, 2026. 
## HOWEVER, as you can see the predicted time is negative! 
So to get an accurate time, I simply printed the date when Xuanyi Geng will break the current world record solely based on his improvement compared to the current world record (3.13).  <br> It will output when his improvement will pass the world record time.  <br>
**It outputs that Xuanyi Geng's improvement will "break" the record (<3.13) on November 1st, 2024.**

### There is a [repl](https://replit.com/@weafcodes/Predicting-the-next-Rubiks-cube-world-record) on replit.com for this


