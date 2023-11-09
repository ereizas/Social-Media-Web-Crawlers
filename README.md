# 4c API Crawler
Used https://github.com/4chan/4chan-API for request commands and example responses

## Use of Rules (as outlined in the link above):
1. Code adheres to 1 request per second
2. Did not use this one since I did not know how to
3. The first function creates the specified header but it seemed useless (did not have any effect)

## Term of Service:
1. This is purposely not called "4chan API Crawler" because the name "4chan" is not permitted

## Functions in 4c API Crawler:
1. Look at "Use of Rules" #3
2. getBoardList() returns a list of board IDs that are required in the following functions requests
3. getArchivedThreadList(board) returns a list of threads (ints) that have been archived for the parameter board. These may or may not be within the desired date range of threads that are to be extracted. I did not check that; I included them in case and to reduce run time (by not checking their threads' last updated dates and eliminating them if so). You can go through and see if all the boards archived threads are within the desired date range and if they are all outside of the range, you can stop using this archived thread list function (assuming the program worked for its runs that considered the earliest date range)
4. getCurrentThreadList(board,deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks) returns a comprehensive thread list for the given board within the specified range of time from the start run time of the function
5. getThreadData(board,threadNum) returns the json file for a thread (stream of comments) for the given board that the threadNum is in
6. getCompleteThreadList(board,deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks) returns the combined list of current and archived threads lists that are returned from the function in #3 and #4
7. getEarliestDateDeltas(csvFile) returns the earliest date in a csvFile formatted the same way as the csv file in this folder. Can add a parameter "valueName" and replace instances of "published_time" with "valueName" in the function for more generality. Dates will have to be in month/date/year hour:minute format for this to work. This is to make sure we get the earliest dated threads needed when first running the program for collection of data.
8. updateCSV(fileName) updates the csv file according to how many threads each link appears and how many replies do the threads have that the links appear in. You must read the comments to edit this function accordingly. Check the comments to see what needs to be done after a successful first run

## To Do List:
1. Find out how and where to the organization/Temple wants to extract comments from threads that have the article urls
2. Run updateCSV successfully for the first time
3. Run updateCSV function according with the start date of the last run as the parameter

## Things to consider:
1. The data collected may only be an estimate of actual values since in the span of the 3 days (maybe less since it was edited for efficiency) this program takes to run, users can post new comments, so there is a chance of missing data to collect

