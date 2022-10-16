#cannot name it the actual social media title because it is forbidden in the API rules
import requests
from datetime import datetime,timedelta, date
import time
import csv
import pandas as pd

#generates required header as mentioned in the github doc and should allow us to choose data based on when it was last modified, but does not work
def generateIfModSinceHeader(deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks):
    #+4 to deltaHours is to account for GMT the required HTML timezone
    dateModSince = datetime.now()-timedelta(seconds=deltaSeconds,minutes=deltaMinutes,hours=deltaHours+4,days=deltaDays,
    weeks=deltaWeeks)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    header = {"If-Modified-Since":str(days[dateModSince.weekday()])+", " + str(dateModSince.day) + " "
     +str(datetime.strptime(str(dateModSince.month),"%m").strftime("%b")) + " " + str(dateModSince.year) + " " + str(dateModSince.time())[0:8]
     + " " + "GMT"}
    print(header["If-Modified-Since"])
    return header

#returns list of unique board IDs that are deemed safe-for-work
#can use the boards in this list as the "board" parameter in the following functions
def getBoardList():
    #keeping track of fxn run time and making it sleep makes sure we do not make more than 1 request per second
    startTime = time.time()
    response  =requests.request("GET","https://a.4cdn.org/boards.json")
    data = response.json()
    #conditional at the end only allows worksafe boards
    boardList = [board['board'] for board in data["boards"] if board["ws_board"]]
    endTime = time.time()
    if(endTime-startTime<1):
        time.sleep(1-(endTime-startTime))
    return boardList

#retrieves list of IDs of archived threads for the given board
def getArchivedThreadList(board):
    startTime = time.time()
    response = requests.request("GET","https://a.4cdn.org/"+board+"/archive.json")
    endTime = time.time()
    if(endTime-startTime<1):
        time.sleep(1-(endTime-startTime))
    data = response.json()
    return data


#comprehensive list of threads for a board, picks out only recently modified threads as specified by the "delta" parameters
def getCurrentThreadList(board,deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks):
    threadList = []
    startTime = time.time()
    response = requests.request("GET","https://a.4cdn.org/"+board+"/threads.json")
    data = response.json()
    for page in data:
        for thread in page['threads']:
            #can add a conditional about number if replies if desired
            if(thread['last_modified']>=time.time()-deltaSeconds-60*deltaMinutes-3600*deltaHours-86400*deltaDays-604800*deltaWeeks): 
                threadList.append(thread['no'])
    endTime = time.time()
    if(endTime-startTime<1):
        time.sleep(1-(endTime-startTime))
    return threadList

#returns the json file from the thread
def getThreadData(board,threadNum):
    startTime = time.time()
    response = int()
    try:
        response = requests.request("GET","https://a.4cdn.org/"+board+"/thread/"+str(threadNum)+".json")
    except Exception as e:
        print(f"Failed to get thread data from {'https://a.4cdn.org/'+board+'/thread/'+str(threadNum)+'.json'}")
        return 0
    #if(response.status_code>200):
       #return 0
    data=response.json()
    endTime = time.time()
    if(endTime-startTime<1):
        time.sleep(1-(endTime-startTime))
    return data

#combines current threads and archived threads into one list
def getCompleteThreadList(board,deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks):
    threads = getCurrentThreadList(board,deltaSeconds,deltaMinutes,deltaHours,deltaDays,deltaWeeks)
    archivedThreads = getArchivedThreadList(board)
    threads.extend(archivedThreads)
    return threads

#finds the earliest date for the deltaTime params in above functions
def getEarliestDateDeltas(csvFile):
    file = pd.read_csv(csvFile)
    earliestDate = datetime.today().date()
    for row in range(len(file)):
        if(type(file.loc[row,'published_time'])==str):
            articleDate=file.loc[row,'published_time']
            articleDate = articleDate[:articleDate.rfind(" ")]
            dateTimeParams = []
            dateTimeParams.append(int(articleDate[len(articleDate)-4:]))
            dateTimeParams.append(int(articleDate[:articleDate.index('/')]))
            dateStr = articleDate[articleDate.index('/')+1:]
            dateTimeParams.append(int(dateStr[:dateStr.index('/')]))
            formattedArticleDate = date(dateTimeParams[0],dateTimeParams[1],dateTimeParams[2])
            if(date.today()-formattedArticleDate>date.today()-earliestDate):
                earliestDate = formattedArticleDate
    return earliestDate


def findThreadsWithuRLsinCSV(fileName):
    op = open(fileName,'r',encoding="utf8")
    csvReader = csv.DictReader(op)
    articles = []
    for row in csvReader:
        articles.append({'id':row['\ufeffid'],'title':row['title'],'url':row['url'],'published_time':row['published_time'],
        '4chan_thread_count':0,'4chan_comment_count':0})
    op.close()
    deltaDaysEarliestDate = date.today()-getEarliestDateDeltas('ArticlesToCheck.csv')
    boardList = getBoardList()
    for board in boardList:
        for thread in getCompleteThreadList(board,0,0,0,deltaDaysEarliestDate.days+1,0):
            data = getThreadData(board,thread)
            if(data!=0):
                for a in range(len(articles)):
                    for post in data['posts']:
                        if('sub' in post and articles[a]['url'] in post):
                            articles[a]['4chan_thread_count'] +=1
                            articles[a]['4chan_comment_count'] = data['posts'][0]['replies']
                            print("hello")
                            break
                        if('com' in post and articles[a]['url'] in post):
                            articles[a]['4chan_thread_count'] +=1
                            articles[a]['4chan_comment_count'] = data['posts'][0]['replies']
                            print('hi')
                            break
                


findThreadsWithuRLsinCSV('ArticlesToCheck.csv')

'''count = 0
boardList = getBoardList()
for board in boardList:
    count+=len(getCompleteThreadList(board,0,0,0,223,0))
print(count)'''
