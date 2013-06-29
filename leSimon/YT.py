import requests
import json
import re

def splitthousands(s, sep=','):  
    if len(s) <= 3: return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]

class YT(object):
    def Main(self, vidId):
        if not vidId:
            return None
        r = requests.get("http://gdata.youtube.com/feeds/api/videos/{0}?alt=json&v=2".format(vidId))
        try:
            r.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError):
            return None
        r = json.loads(r.text)
        return self.Parse(r)
        
    def ConvertTime(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        duration = ""
        if hours != 0:
            duration += "{0}:".format(str(hours).zfill(2))
        duration += "{0}:{1}".format(str(minutes).zfill(2), str(seconds).zfill(2))
        return duration
        
    def Parse(self, reply):
        if 'gd$rating' in reply['entry']:
            return {'title': reply['entry']['title']['$t']
                ,'duration': self.ConvertTime(int(reply['entry']['media$group']['yt$duration']['seconds']))
                ,'author': reply['entry']['author'][0]['name']['$t']
                ,'averagerating': str(reply['entry']['gd$rating']['average'])[:4]
                ,'maxrating': reply['entry']['gd$rating']['max']
                ,'numLikes': reply['entry']['yt$rating']['numLikes']
                ,'numDislikes': reply['entry']['yt$rating']['numDislikes']
                ,'viewCount': splitthousands(reply['entry']['yt$statistics']['viewCount'])}
        else:
            return {'title': reply['entry']['title']['$t']
                ,'duration': self.ConvertTime(int(reply['entry']['media$group']['yt$duration']['seconds']))
                ,'author': reply['entry']['author'][0]['name']['$t']
                ,'viewCount': splitthousands(reply['entry']['yt$statistics']['viewCount'])}

def Stats(data):
    vidIds = list(set(re.findall("v=([a-zA-Z0-9_\-]{11})", data)))
    for vidId in vidIds:
        L = YT()
        x = L.Main(vidId)
        if x != None:
            info = "\x02[YouTube]\x02 {0}".format(x['title'])
            info += " - By: \x02{0}\x02".format(x['author'])
            info += " [\x02{0}\x02]".format(x['duration'])
            if 'averagerating' and 'maxrating' in x:
                info += " - \x02{0}\x02/\x02{1}\x02".format(x['averagerating'], x['maxrating'])
            info += " - \x02{0}\x02 Views".format(x['viewCount'])
            if 'numLikes' and 'numDislikes' in x:
                info += " - \x02{0}\x02 Likes".format(x['numLikes'])
                info += " - \x02{0}\x02 Dislikes".format(x['numDislikes'])
            return info
        else:
            return None