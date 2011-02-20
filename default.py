
import xbmcplugin,xbmcgui,xbmcaddon
import urllib2,urllib,re,os
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.gamekult')
__home__ = __settings__.getAddonInfo('path')

DEFAULT_THUMB  = xbmc.translatePath( os.path.join( __home__, 'resources/gamekult.png' ) )
EMISSION_THUMB = xbmc.translatePath( os.path.join( __home__, 'resources/emission.jpg' ) )


SITE   = 'http://www.gamekult.com' 

# plugin handle
HANDLE = int(sys.argv[1])


def getShows():

	addDir('L\'émission',SITE + '/video?t=emission',1, EMISSION_THUMB)
	addDir('Tests',SITE + '/video?t=test',1, DEFAULT_THUMB)
	addDir('Gameplay',SITE + '/video?t=gameplay',1, DEFAULT_THUMB)
	addDir('Trailers',SITE + '/video?t=trailers',1, DEFAULT_THUMB)
	addDir('Rétro',SITE + '/video?t=retro',1, DEFAULT_THUMB)

def getEpisodes(dir_url,name):

    	content = getUrl(dir_url)

	matched_urls  = re.compile('<li>\\n\\t\\t\\t<a href="(.*?)" class="clearfix clear left w1">.*?</a>', re.DOTALL).findall(content)
	
	nb_items = len(matched_urls)

	for  url in matched_urls:

		clip  = getClip(getClipXmlUrl(SITE + url))

		if clip is not None:
			addLink(clip[0],clip[1],clip[2],nb_items)   

def getClipXmlUrl(url):
	# http://www.gamekult.com/video/marvel-vs-capcom-3-fate-of-two-worlds-annonce-sentinel-10330448v.html
	id = re.search(r'.+\-(.+?)v\.html',url).group(1)
	# http://www.gamekult.com/videos/video_xml/10330448-pegi=;jeune=0;-0-bill
	return "http://www.gamekult.com/videos/video_xml/%s-pegi=;jeune=0;-0-bill" % id

def getClip(url):

	content = getUrl(url)
	soup = BeautifulSoup(content, convertEntities=BeautifulSoup.XML_ENTITIES)
	track = soup.findAll('track')[1]
	title = track.annotation.contents[0].replace('video du jeu','').replace('sur  :','').strip()
	flv = track.location.contents[0]
	img = track.image.contents[0]
	return [title,flv,img]

def get_params():

	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	
	return param


def addLink(name,url,iconimage,nb_items):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=HANDLE,url=url,listitem=liz, totalItems=nb_items)
	return ok



def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=HANDLE,url=u,listitem=liz,isFolder=True)
	return ok


def getUrl(url):
	req = urllib2.Request(url)
	req.addheaders = [('Referer', SITE), ('Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13')]
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


params=get_params()
url=None
name=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
	getShows()
	
elif mode==1:
	print ""+url
	getEpisodes(url,name)

xbmcplugin.endOfDirectory(HANDLE)	

