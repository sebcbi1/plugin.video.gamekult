
import xbmcplugin,xbmcgui,xbmcaddon
import urllib2,urllib,re,os

SITE   = 'http://www.gamekult.com' 
URL    = '/video?t=emission'

# plugin handle
HANDLE = int(sys.argv[1])


def show_root_menu():

	pDialog = xbmcgui.DialogProgress()
  	ret = pDialog.create('Gamekult, l\'émission', 'Retrieving items...', '')

    	content        = getUrl(SITE + URL)
	matched_urls   = re.compile('<li>\\n\\t\\t\\t<a href="(.*?)" class="clearfix clear left w1">.*?</a>', re.DOTALL).findall(content)
	matched_descr  = re.compile('<span class="tQuiet left clear w100">.+?<br/>(.+?)</span>', re.DOTALL).findall(content)
	matched_titles = re.compile('<span class="tMedium tLoud tLeft tBlack">(.+?)</span>', re.DOTALL).findall(content)
	matched_images = re.compile('<span style="background: url\(\'(.+?)\'\) no-repeat scroll center center transparent;" class="left height110 w12 borderS borderGrey"></span>', re.DOTALL).findall(content)
	
	nb_items = len(matched_urls)
	
	ret = pDialog.update(0, 'Retrieving items...', '0 of %i' % nb_items)

	matched_flvs = []

	for  i, url in enumerate(matched_urls):

		content = getUrl(SITE + url)
		match=re.compile('<link rel="video_src" href="(.+?)"/>', re.DOTALL).findall(content)

		if len(match)==1:
		   match2=re.compile('xspf=(.+?)&', re.DOTALL).findall(match[0])

		   if len(match2)==1:
		      	content = getUrl(match2[0])
			match3=re.compile('<track>.*<location>(.+?)</location>.*<annotation>.*</annotation>.*</track>', re.DOTALL).findall(content)
	
			if len(match3)==1:
				matched_flvs.append(match3[0])
				
				url = matched_urls[i]
				title = matched_titles[i].strip() 
				img = matched_images[i]
				flv = matched_flvs[i]
				description = matched_descr[i]
				addLink(title,flv,img,description)          
	
		ret = pDialog.update(int((100/nb_items*(i+1))+0.5), 'Retrieving items...', '%i of %i' % ((i+1),nb_items))
		if pDialog.iscanceled():
		    return 0

	xbmcplugin.endOfDirectory(handle=HANDLE, succeeded=True)

def addLink(name,url,iconimage,description):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'Plot' : description } )
		ok=xbmcplugin.addDirectoryItem(handle=HANDLE,url=url,listitem=liz)
		return ok

def getUrl(url):
    req = urllib2.Request(url)
    req.addheaders = [('Referer', SITE), ('Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13')]
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

ok = show_root_menu()

xbmcplugin.endOfDirectory(HANDLE)	

