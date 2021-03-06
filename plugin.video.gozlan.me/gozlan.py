# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from gozlan.me
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
from xml.sax import saxutils as su
import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()

##General vars
__plugin__ = "gozlan.me"
__author__ = "Cubicle"

__image_path__ = ''
# Don't forget to set lib/gozlanurlresolver/common.py
__settings__ = xbmcaddon.Addon(id='plugin.video.gozlan.me')
addon = __settings__ 
__language__ = __settings__.getLocalizedString
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__BASE_MOVIES_PATH__ = 'Z:\\Movies\\New\\downloads';
__devel__ = 0
#base_domain="http://deniro.me"
#base_domain = "http://anonymouse.org/cgi-bin/anon-www.cgi/http://deniro.me"
base_domain = "http://gozlan.co"

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'lib' ) )
sys.path.append (LIB_PATH)
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'lib' ) )
sys.path.append (LIB_PATH)

from gozlancommon import *
from t0mm0.common.net import Net
#from gozlanurlresolver import *
import urlresolver

# Tmp
#print 'sys.argv[2]' + str(sys.argv[2])
#print 'sys.argv='+str(sys.argv)

params = getParams(sys.argv[2])
url=None
name=None
mode=None
module=None
page=None


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
try:
        module=urllib.unquote_plus(params["module"])
except:
        pass
try:
        page=urllib.unquote_plus(params["page"])
except:
        pass


def gozlan_movie_categories(url):
  page=getData(url,0)
  #<li><a href="search.html?g=הרפתקאות">סרטי הרפתקאות</a></li>
  regexp='<li><a href="[^"]*?search.html\?(\w+)=(.*?)">(.*?)</a></li>'
  matches = re.compile(regexp).findall(page)
  for match in matches:
      results_cat=match[0]
      results_crit=match[1]
      results_page=match[0]+"="+urllib.quote(results_crit)
      cat_name=match[2]
      #print "results_page="+results_page+"; cat_name="+cat_name
      addDir(cat_name,base_domain+"/search.html?"+results_page,"1&content=movies",'')
  xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def gozlan_series(url):
  page=getData(url,1)
  #<a href="ser.php?ser=האגדה%20של%20קורה">
	#		<img src="movpics/4feddfb532688.jpg" alt="seriesImage" />
	#		<span class="serName">האגדה של קורה</span>
	#<li style="width:153px"><div class="pic_top_movie2"><a href="vseries.html?id=127"><img src="http://gozlan.me/uploads/50c9cfb938aab.jpg" alt="The Voice ישראל לצפייה ישירה" /></a></div><div class="text_banner_top2"><a href="vseries.html?id=127">The Voice ישראל</a></div>
  regexp='<a href="(vser.*?)"><img src="(.*?)" alt=".*?<a href.*?">(.*?)</a></div>'
  matches = re.compile(regexp).findall(page)
  for match in matches:
      series_page=match[0]
      icon=match[1]
      name=match[2]
      # print "series_page="+series_page+"; icon="+icon+"; name="+str(name)
      if ((series_page.find('http'))<0):
        series_page = base_domain+'/'+series_page
      addDir(name ,series_page,'6&icon='+urllib.quote(icon),icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

def gozlan_series_seasons(url):
  page=getData(url,7)
  #						<div class="bmovie4">
	#						<a href="ser.php?ser=24&se=1">עונה: 1</a>
	#					</div>
  block_regexp='<h2>עונות:</h2>(.*?)<div class="foot"'
  block_matches = re.compile(block_regexp).findall(page)
  #print block_matches[0]
  regexp='href="search.html\?s=(.+?)">'
  icon=urllib.unquote_plus(params["icon"])
  matches = re.compile(regexp).findall(block_matches[0])
  for match in matches:
      season_page="search.html?s="+urllib.quote(match)
      name=match
      #print "season_page="+season_page+"; icon="+icon+"; name="+str(name)
      if ((season_page.find('http'))<0):
        season_page = base_domain+"/"+season_page
      addDir(name ,season_page,'1&icon='+urllib.quote(icon),icon)
  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
  
  
def gozlan_video_types():
  if __devel__:
    addVideoLink('test-sockshare', 'http://www.sockshare.com/embed/67CF7956B246AB8E', 2, '' )
    addVideoLink('test-novamov', 'http://embed.novamov.com/embed.php?v=tverz6xc4slbe&px=1', 2, '' )
    addVideoLink('test-series-novamov', 'http://www.moviex-il.com/series.php?serid=2303', 2, '' )
    #http://www.youtube.com/embed/jzCYuflJWas
    addVideoLink('test-youtube', 'http://www.moviex-il.com/movie-%D7%A7%D7%95%D7%A4%D7%99%D7%9D-%D7%91%D7%97%D7%9C%D7%9C-2.html', 2, '' )
    addDir('search: תזיזו', 'תזיזו', 8, '' )
  addDir('סרטים',base_domain+'/search.html?t=movie',4,'')
  #addDir('סדרות',base_domain+'/search.html?t=series',5,'')
  addDir('סדרות',base_domain+'/series.html',5,'')
  addDir('חיפוש סרטים','Movies',9,'')
      
def gozlan_search_page(url):
    content="tvshows"
    if "content" in params:  
      content=params["content"]
    page_no=1
    if ("page_no" in params):
      page_no=int(params["page_no"])
    next_page_no=str(page_no+1)
    page=getData(url,0)
    #print page
    #<div class="movie_pic"><a href="האי-של-נים-מדובב-לעברית--לצפייה-ישירה-3831.html"><img src="uploads/50c928afbc30c.jpg" width="105" height="156" alt="האי של נים-מדובב לעברית- לצפייה ישירה" /></a></div>
    derug = '\xd7\x93\xd7\x99\xd7\xa8\xd7\x95\xd7\x92'
    #regexp = '<div class="movie_pic">.*?<img src="(.*?)" width.*?<strong>.*?<h2><a href="(.*?)">(.*?)</a></h2>'
    #regexp = '<div class="movie_pic">.*?<img src="(.*?)" width.*?<strong>.*?<h2><a href="(.*?)">(.*?)</a></h2>.*?\s('+derug+': <span>(.*?)</span>)+?'
    regexp = '<div class="movie_pic">.*?<img src="(.*?)" width.*?<strong>.*?<h2><a href="(.*?)">(.*?)</a></h2>.*?'+derug+': <span>(.*?)</span>'
    #class="pagenum"><a href="/search.html?s=%D7%9E%D7%93%D7%95%D7%91%D7%91&p=2">2</a>  
    next_page_regexp='<a href="(\/search\.html[^"]*?&p='+next_page_no+')">'+next_page_no
    matches = re.compile(regexp,re.M+re.I+re.S).findall(page)

    #matches_genres = re.compile('class="c">(.*?)</div>',re.M+re.I+re.S).findall(page)
    summary = ''                
    for match in matches:
      image=match[0]
      page_link=match[1]
      name=match[2]
      #print "page_link="+page_link+"; name="+name+"; image="+image+"\n"
      addDir(name + " [" + match[3]+"]",page_link,"2&conetnt="+urllib.quote(content)+"&name="+urllib.quote(name)+"&image="+urllib.quote(image),base_domain+"/"+image, '', summary)
    if (len(matches)<1): # No matches -> maybe new sdarot format
      regexp = '<div class="movie_pic"><a href="(.*?)"><img src="(.*?)" width.*?alt="(.*?)"/></a>'
      matches = re.compile(regexp,re.M+re.I+re.S).findall(page)
      for match in matches:
        image=match[0]
        page_link=match[1]
        name=match[2]
        #print "page_link="+page_link+"; name="+name+"; image="+image+"\n"
        addDir(name,page_link,"2&conetnt="+urllib.quote(content)+"&name="+urllib.quote(name)+"&image="+urllib.quote(image),base_domain+"/"+image, '', summary)
    next_page_matches = re.compile(next_page_regexp).findall(page)
    if (len(next_page_matches) > 0):
      next_page_url=base_domain+ su.unescape(next_page_matches[0])
      print "\nNext Page: "+next_page_url+" (matches="+next_page_matches[0]+")\n"
      addDir("עוד...",next_page_url,"1&conetnt="+urllib.quote(content)+"&page_no="+next_page_no,'')
    else:
      print "No next page. URL=" + url + ";regexp=" + next_page_regexp + "\n"
    xbmcplugin.setContent(int(sys.argv[1]), content)

def gozlan_play_video(url):
    name = url
    if ("name" in params):
      name=params["name"]
    image=""
    if ("image" in params):
      image=params["image"]
    description=""
    if "description" in params:  
      description=params["description"]
    print url
    if ((url.find(base_domain))<0):
        url = base_domain+'/'+url
    page=getData(url,7)

    # <iframe src="http://www.putlocker.com/embed/F4988CE321910D0D" id='iframeinner'
    regexp='<iframe src="(.*?)" id=\'iframeinner\''
    media_url=re.compile(regexp,re.M+re.I+re.S).findall(page)[0]
    q=media_url.find('http',1)
    if q > 0:
        media_url = media_url[q:]
    print "Resolving URL: " + media_url
    videoPlayListUrl = urlresolver.HostedMediaFile(url=media_url).resolve()
    if not videoPlayListUrl:
      print "URL " + media_url + " could not have been resolved to a movie.\n"
      return
    #addon.resolve_url(stream_url)
    #videoPlayListUrl = urllib.unquote(videoUrl[0])
    listItem = xbmcgui.ListItem(name, image, image, path=videoPlayListUrl) # + '|' + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    listItem.setInfo(type='Video', infoLabels={ "Title": name})
    listItem.setProperty('IsPlayable', 'true')
    print "video url " + videoPlayListUrl
    #xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(videoPlayListUrl)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def gozlan_video_page(url):
    name = urllib.unquote(url)

    if ("name" in params):
      name=urllib.unquote(params["name"])
    image=""
    if ("image" in params):
      image=params["image"]
    description=""
    if "description" in params:  
      description=params["description"]
    content="tvshows"
    if "content" in params:  
      content=params["content"]
    #print "gozlan_video_page (name): "+name
    #print "Calling getdata("+base_domain+"/"+url+")\n"
    if (url.find('http')<0):
            url = base_domain+"/"+url
    page = getData(url,3)
    curr_source = 0
    # <meta property="og:description" content="הסרט הרווקה עכשיו לצפייה ישירה עם תרגום מובנה בחינם ובמהירות! תקציר הסרט: בקי מתחנת והיא בוחרת בשלוש חברות שנהגו ללעוג לה בתיכון להיות השושבינות שלה לחתונה ולארגן לה את מסיבת הרווקות.שלוש החברות רגן, קייט וג'נה מתכננות את חתונתה של בקי שהייתה המטרה שלהן להקנטות בתיכון , לאחר שהיא מינתה אותן כשושבינות לחתונה שלה." />
    description= re.compile('<meta property="og:description" content="(.*?)"',re.M+re.I+re.S).findall(page)[0]
    #<span class="quality_button"><img style="margin-top:-3px;position:relative;width:100px;height:32px" src="http://s.ytimg.com/yts/img/logos/youtube_logo_standard_againstwhite-vflKoO81_.png" alt="Youtube" /></span><span class="quality_button">720p</span><span class="playing_button"><a  href="play/4537/גוללל-סטאר-עונה-1-פרק-29-לצפייה-ישירה-3884.html"><img style="margin-top:-3.2px;position:relative" src="index_files/watch.jpg" alt="גוללל סטאר עונה 1 פרק 29 לצפייה ישירה" /></a><font id="edit_462635"></font></span>
    #<span class="quality_button"><img style="margin-top:-3px;position:relative;width:110px" src="logo_novamov.jpg" alt="Novamov" /></span><span class="quality_button">DVDRip</span><span class="playing_button"><a  href="play/4826/2-צעדים-למוות-לצפייה-ישירה-4077.html"><img style="margin-top:-3.2px;position:relative" src="index_files/watch.jpg" alt="2 צעדים למוות לצפייה ישירה" /></a><font id="edit_462635"></font></span>

    tmp = re.compile("<h1>(.*?)</h1>").findall(page)[0]
    engname = tmp[tmp.find('/')+1:].strip()
    engname = engname.replace(':','_')
    #print "tmp="+tmp
    #print "engname="+engname

    # imdb ref
    tmp = re.compile('href="(http://imdb.com/title/tt\d*?)/"').findall(page)
    if len(tmp) > 0:
        imdbref = tmp[0]
    else:
        imdbref = ''

    regexp = 'quality_button\"><img.*?src=".*?" alt="([\w|0-9]+?)"\s*/></span><span class="quality_button">(.*?)</span><span\s+?class="playing_button"><a\s+?href="(.*?)"'  
    regexp2 = 'quality_button\"><strong[^>]*?>(.*?)</strong></span><span class="quality_button">(.*?)</span><span\s+?class="playing_button"><a\s+?href="(.*?)"'  
    matches = re.compile(regexp).findall(page)
    matches2 = re.compile(regexp2).findall(page)
    if len(matches2) > 0:
            for match in matches2:
                    matches.append(match)
    if len(matches) > 0:
      for match in matches:
        provider_image='' #match[0]
        #if ( provider_image.find("http:") == -1 ):
          #provider_image=base_domain+"/"+provider_image
        provider_name=match[0]
        provider_quality=match[1]
        video_page_link=match[2]
        print "provider_image: "+provider_image+"; provider_name: "+provider_name+"; provider_quality: "+provider_quality+"; video_page_link: " + video_page_link
        
        addVideoLink(name + " דרך " + provider_name + " [[B]"+provider_quality+"[/B]]" ,video_page_link,"&engname="+engname+"&imdbref="+imdbref,"3&name="+urllib.quote(name)+"&image="+urllib.quote(image)+"&description="+urllib.quote(description),base_domain+"/"+image,description)
    else:
      print "No matches for "+regexp+"\n"
    #<span class="quality_button"><strong style="font-family:'Cuprum',sans-serif; font-weight:bold; font-size:18px;color:Aqua">VideoSlasher</strong></span><span class="quality_button">BDRip</span><span class="playing_button"><a  href="play/4375/2012--עידן-הקרח-לצפייה-ישירה-3533.html"><img style="margin-top:-3.2px;position:relative" src="index_files/watch.jpg" alt="2012: עידן הקרח לצפייה ישירה" /></a><font id="edit_462635"></font></span>
##    regexp = 'quality_button.*?<strong.*?>(.*?)</strong></span>.*?_button">(.*?)</span><span class="playing_button"><a  href="(.*?)"'  
##    matches = re.compile(regexp).findall(page)
##    curr_source = 0
##    if len(matches) > 0:
##      for match in matches:
##        provider_image=""
##        provider_name=match[0]
##        provider_quality=match[1]
##        video_page_link=match[2]
##        #print "provider_image: "+provider_image+"; provider_name: "+provider_name+"; provider_quality: "+provider_quality+"; video_page_link: " + video_page_link
##        addVideoLink(name + " דרך " + provider_name + " [[B]"+provider_quality+"[/B]]" ,video_page_link,"&engname="+engname,"3&name="+urllib.quote(name)+"&image="+urllib.quote(image)+"&description="+urllib.quote(description),base_domain+"/"+image,description)
##    else:
##      print "No matches for "+regexp+"\n"
    xbmcplugin.setContent(int(sys.argv[1]), content)

def gozlan_download(url, params):
    engname=params["engname"]
    imdbref=params["imdbref"]
    #print "params="+str(params)
    # xbmcgui.Dialog().ok("Params" , str(params))
    if (url.find('http')<0):
            url = base_domain+"/"+url
    page=getData(url,7)
    # <iframe src="http://www.putlocker.com/embed/F4988CE321910D0D" id='iframeinner'
    regexp='<iframe src="(.*?)" id=\'iframeinner\''
    media_url=re.compile(regexp,re.M+re.I+re.S).findall(page)[0]
    #print "Resolving URL: " + media_url
    videoPlayListUrl = gozlanurlresolver.HostedMediaFile(url=media_url).resolve()
    if not videoPlayListUrl:
      print "URL " + media_url + " could not have been resolved to a movie.\n"
      return
    #addon.resolve_url(stream_url)
    #videoPlayListUrl = urllib.unquote(videoUrl[0])
    #print "video url " + videoPlayListUrl

    vurl = videoPlayListUrl #videoPlayListUrl[1:videoPlayListUrl.find('|')]
    movie_name = engname
    dwldPath = xbmc.translatePath(os.path.join(__BASE_MOVIES_PATH__, "%s"%(movie_name)))
    if not os.path.exists(dwldPath):
        os.makedirs(dwldPath)
    if (vurl.find(".flv") > 0):
        filename = engname + ".flv"
    elif (vurl.find(".mp4") > 0):
        filename = engname + ".mp4"
    else :
        filename = engname+".avi"

    # Save nfo file
    if len(imdbref) > 1:
        text_file = open(dwldPath+'\\'+engname+".nfo", "w")
        text_file.write(imdbref)
        text_file.close()
    
    prms = { "url": vurl, "download_path": dwldPath, "Title": movie_name }
    print "downloading %s from %s to %s"%(movie_name, vurl,dwldPath+'\\'+engname)
    # downloader.dbg = True
    downloader.download(filename, prms)
      
def gozlan_search_dialog(url):
    searchtext=""
    keyboard = xbmc.Keyboard(searchtext, 'חיפוש סרט')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        #searchtext = urllib.quote_plus()
        gozlan_search_page(base_domain+"/search.html?s="+keyboard.getText())        

if mode==None:
    gozlan_video_types()      
elif mode==1:
    gozlan_search_page(url)
elif mode==2:
    gozlan_video_page(url)
elif mode==3:
    gozlan_play_video(url)
elif mode==4:
    gozlan_movie_categories(url)
elif mode==5:
    gozlan_series(url)
elif mode==6:
    gozlan_series_seasons(url)
elif mode==9:
    gozlan_search_dialog(url)
elif mode==10:
    gozlan_download(url, params)
#
#elif mode==3:
#    EPISODES(url, module)
#
#elif mode==4:
#    PLAY_MOVIE(url, name)
#
#elif mode==5:
#    SHOWING_NOW(url)   
#          
#else:
#    GENRES()

xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__,"fanart.jpg") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=0)
