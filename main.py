import historyofwr
# ^ Creates the wrhistory.csv file. This world record data will be used later on to predict the new world record.

import getCandidateData
# ^ This file creates the contendersRecentSolves.csv file. It will get the contenders for the world record, then get the last 50 solves. These are the solves that will be used to find the best cuber in parseData.py.

import parseData
# ^ This file creates the contendersParsedDatacsv file. The csv contains the variables of the solves, like the fastest solve out of the recent solves, from the contendersRecentSolves.

import finalpredict
# ^ This uses wrhistory.csv and contendersParsedData and finds each cuber's score. It will find the best cuber based on that score. You can check the contendersScoreLeadboard.csv for every cuber. Then it uses the wrhistory.csv and graphs it's progression, and graphs the best cuber's personal record progression. Lastly, it finds the intersection and gets the prediction.
