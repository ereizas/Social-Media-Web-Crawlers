import requests
import bs4 as bs

def getSiteUUID(url):
    domain = ''
    for char in url[url.find('/')+2:]:
        if(char=='/'):
            break
        domain+=char
    response = requests.request('POST','https://api.viafoura.co/v2/' + domain + '/bootstrap/v2')
    data = response.json()
    return data['result']['settings']['site_uuid']

def getExpressIDNum(url):
    startInd = url.rfind('/')
    idReversed = ''
    for i in range(startInd-1,0,-1):
        if(url[i]=='/'):
            break
        idReversed+=url[i]
    id = [char for char in reversed(idReversed)]
    return ''.join(id)
    
def getIDthruHTML(url,attr):
    response = requests.request("GET",url)
    print(response.status_code)
    soup = bs.BeautifulSoup(response.text,'html.parser')
    metaLineWithID = str(soup.find('meta',attrs=attr))
    id=''
    for i in range(metaLineWithID.find('content=')+9,len(metaLineWithID)):
        if(metaLineWithID[i]=='"'):
            break
        id +=metaLineWithID[i]
    return id
    


def getComments(url):
    containerID = str()
    #conditionals handle different news outlets container ids
    #CBC and Philadelphia Inquirer did not work even though they had clear unique ids 
    # (found by searching for "vf:" in html and the unique id was usually one of the first results)
    if('independent.co' in url):
        containerID = url[url.rfind('-')+1:url.rfind('.')]
    elif('mirror.co' in url):
        containerID = 'mirror-prod-' + url[url.rfind('-')+1:]
    elif('dailystar.co' in url):
        containerID = 'dailystar-prod-' + url[url.rfind('-')+1:]
    elif('clarin.com' in url):
        containerID = url[url.rfind('_')+1:url.rfind('.')]
    elif('nationalpost.com' in url or 'mercurynews.com' in url or 'lanacion.com' in url or 'pressdemocrat.com' in url):
        containerID = getIDthruHTML(url,{'name':'vf:container_id'})
    elif('20minutes.fr' in url):
        containerID = url[url.rfind('/')+1:url.find('-')]
    elif('express.co' in url):
        containerID = 'express-prod-' + getExpressIDNum(url)
    elif('sportsnet.ca' in url):
        containerID = 'post-' + getIDthruHTML(url,{'name':'sn-post-id'})
    elif('xtramagazine.com' in url):
        containerID = url[url.rfind('-')+1:]+'_post'
    elif('thestar.com' in url):
        containerID=getIDthruHTML(url,{'property':'vf:unique_id'})
    elif('telegraph.co' in url):
        containerID = getIDthruHTML(url,{'property':'vf:container_id'})
    elif('clickondetroit.com' in url):
        containerID= getIDthruHTML(url,{'name':'vf:unique_id'})
    else:
        return []
    commentData = []
    try:
        response = requests.request('GET','https://livecomments.viafoura.co/v4/livecomments/'+getSiteUUID(url)+'?limit=100&container_id='
        + containerID+'&reply_limit=100&sorted_by=newest')
        commentData.append(response.json())
        finished = False
        ind = 0
        print(commentData)
        #ends up in infinite loop (not sure why this part doesn't work)
        #supposed to get more comments from comment sections with more than 100 comments
        '''while(not finished):
            try:
                lastCommentUUID = commentData[ind]['contents'][len(commentData[ind]['contents'])-1]['content_uuid']
                print(lastCommentUUID)
                response = requests.request('GET','https://livecomments.viafoura.co/v4/livecomments/'+getSiteUUID(url)+'?limit=100&container_id='
                + containerID+'&reply_limit=100&sorted_by=newest&starting_from=' + lastCommentUUID)
                commentData.append(response.json())
                ind+=1
            except:
                finished = True'''
    except:
        return "Website not accessible."
    print(len(commentData))



    return commentData




getComments('https://www.sportsnet.ca/nhl/article/nhl-defends-no-goal-call-on-flames-coleman-it-was-unanimous/')


