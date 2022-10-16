from unicodedata import name
import requests

#might need to use html parsing and beautifulSoup to get more info such as chat info
#if the info from this api is good enough, then I can attempt to program something that gets the info from multiple videos shown from a search
#sees whether a url is in the description
def getVideoInfo(videoID,url):
    url = "https://rumble-videos.p.rapidapi.com/"+videoID
    headers = {
	"X-RapidAPI-Host": "rumble-videos.p.rapidapi.com",
	"X-RapidAPI-Key": "c6b8a06adamshcea1d6540a227d2p1fd9aejsnb0f58273c543"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return data['description'].find(url)!=-1
    
