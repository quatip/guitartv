import re
import requests
import xbmcgui
import xbmcplugin
from resources.lib import truefire
from resources.lib import context

context = context.Context()
provider = truefire.TrueFireProxy(context)
xbmcplugin.setContent(context.addon_handle, 'movies')

def root():
    _addMenuEntry('available')
    _addMenuEntry('educators')
    _addMenuEntry('general_courses')
    xbmcplugin.endOfDirectory(context.addon_handle)

def _addMenuEntry(command, **kwargs):
    li = xbmcgui.ListItem(command)         
    xbmcplugin.addDirectoryItem(handle = context.addon_handle,
                                listitem = li,
                                url = provider.create_url(command, **kwargs),
                                isFolder = True) 

def available():
    _add_courses(provider.available())

def _add_courses(courses_ids):
    educ_dict = dict([ (educ.id, educ) for educ in provider.educators() ])
    for id in courses_ids:
        desc = provider.course_description(id)
        _add_course(desc, educ_dict[desc['AuthorID']])
    xbmcplugin.endOfDirectory(context.addon_handle)

def _add_course(desc, educator):
    info = {}
    release_date = re.search(r'(\d\d)-(\d\d\d\d)', desc['release_date'])
    if release_date:
        year = int(release_date.group(2))
        info['year'] = year

    runningTime = re.search(r'(\d\d):(\d\d)', desc['totalRunningTime'])
    if runningTime:
        duration = int(runningTime.group(1))*60 + int(runningTime.group(2))
        info['duration'] = duration

    title = desc['title']
    info['title'] = title
    info['plot'] = desc['overview']
    info['director'] = educator.name

    li = xbmcgui.ListItem(title)
    li.setInfo('video', info)
    li.setArt({ 'poster' : desc['thumbnailURL'], 'fanart' : desc['videoPreviewImage']})

    url = provider.create_url('course_detail', course_id=desc['id'])
    xbmcplugin.addDirectoryItem(handle = context.addon_handle,
                                listitem = li, url = url, isFolder = True) 


def educators():
    for educator in provider.educators():
        li = xbmcgui.ListItem(educator.name, iconImage=educator.thumbnail)
        li.setInfo('video', {'title': educator.name})
        url = provider.create_url('educator_detail', id=educator.id)
        xbmcplugin.addDirectoryItem(handle = context.addon_handle,
                                    listitem = li, url = url, isFolder = True) 

        xbmcplugin.endOfDirectory(context.addon_handle)
        xbmcplugin.addSortMethod(context.addon_handle, xbmcplugin.SORT_METHOD_TITLE)

def general_courses():
    courses = provider.courses()

    for c in sorted(courses, key=lambda x: x['title']):
        li = xbmcgui.ListItem(c['title'], iconImage=c['thumbnailURL'])        
        url = provider.create_url('course_detail', course_id=c['id'])
        xbmcplugin.addDirectoryItem(
            handle=context.addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(context.addon_handle)


def course_detail(course_id):
    detail = provider.course_detail(course_id)
    course = detail['course']

    validChapters = [chapter for chapter in detail['video_files'] if chapter['videoUrl']]

    print "Valid chapters: {}".format(len(validChapters))

    for chapter in validChapters:
        if chapter['videoUrl']:
            li = xbmcgui.ListItem(chapter['videoTitle'], label2=chapter['videoSubTitle'])
            url = provider.video_url(chapter['videoStreamingUrl'])
            xbmcplugin.addDirectoryItem(handle=context.addon_handle, listitem = li, url = url) 

    xbmcplugin.endOfDirectory(context.addon_handle)


def _addtestinfo(listitem):
    info = { 
        'genre': 'genre',
        'year' : 2012,
        'episode' : 100,
        'season': 1,
        'top250': 500,
        'tracknumber' : 3,
        'rating' : 10,
        'playcount' : 25,
        'overlay' : 8,
        'cast' : ['cast'],
        'castandrole' : ['cast|role'],
        'director' : 'director',
        'mpaa' : 'mpaa',
        'plot' : 'plot',
        'plotoutline' : 'plotoutline',
        'title' : 'title',
        'originaltitle' : 'originaltitle',
        'sorttitle' : 'sorttitle',
        'duration' : 300,
        'studio' : 'studio',
        'tagline' : 'tagline',
        'writer' : 'writer',
        'tvshowtitle' : 'tvshowtitle',
        'premiered' : '2005-03-04',
        'status' : 'status',
        'code' : 'code',
        'aired' : 'aired',
        'credits' : 'credits',
        'lastplayed' : '2009-04-05 23:16:04',
        'album' : 'album',
        'artist' : ['artist'],
        'votes' : 'votes',
        'trailer' : 'trailer',
        'dateadded' : '2009-04-05 23:16:04'
        }

    listitem.setInfo('video', info)


func = globals()[context.get_func()]
nargs = func.func_code.co_argcount
args = func.func_code.co_varnames[0:nargs]
argvalues = [context.get_param(arg) for arg in args]
func(*argvalues)
