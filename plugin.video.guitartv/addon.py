import xbmcgui
import xbmcplugin
from resources.lib import truefire
from resources.lib import context

ctx = context.KodiContext()
proxy = truefire.Proxy(ctx)
xbmcplugin.setContent(ctx.addon_handle, 'movies')


def root():
    _add_menu_entry('available')
    _add_menu_entry('educators')
    _add_menu_entry('new')
    _add_menu_entry('hot')
    _add_menu_entry('general_courses')
    xbmcplugin.endOfDirectory(ctx.addon_handle)


def _add_menu_entry(command, **kwargs):
    li = xbmcgui.ListItem(command)         
    xbmcplugin.addDirectoryItem(handle=ctx.addon_handle,
                                listitem=li,
                                url=proxy.create_url(command, **kwargs),
                                isFolder=True)


def available():
    _add_courses(proxy.available())


def new():
    _add_courses(proxy.recently_added())


def hot():
    _add_courses(proxy.whats_hot())


def general_courses():
    _add_courses(proxy.courses())


def _add_courses(courses):

    xbmcplugin.addSortMethod(ctx.addon_handle, xbmcplugin.SORT_METHOD_TITLE)

    for c in courses:
        info = dict(title=c.title)
        li = xbmcgui.ListItem(c.title)
        li.setInfo('video', info)
        li.setArt(dict(poster=c.thumbnail, fanart=c.fan_art))
        url = proxy.create_url('course_detail', course_id=c.id)
        xbmcplugin.addDirectoryItem(handle=ctx.addon_handle,
                                    listitem=li, url=url, isFolder=True)

    xbmcplugin.endOfDirectory(ctx.addon_handle)


def educators():
    xbmcplugin.addSortMethod(ctx.addon_handle, xbmcplugin.SORT_METHOD_TITLE)
    for educator in proxy.educators():
        li = xbmcgui.ListItem(educator.name, iconImage=educator.thumbnail)
        li.setInfo('video', dict(title=educator.name))
        url = proxy.create_url('educator_detail', educator_id=educator.id)
        xbmcplugin.addDirectoryItem(handle=ctx.addon_handle,
                                    listitem=li, url=url, isFolder=True)

        xbmcplugin.endOfDirectory(ctx.addon_handle)


def course_detail(course_id):
    detail = proxy.course_detail(course_id)

    for chapter in detail.chapters:
        title = chapter.title + ' - ' + chapter.sub_title

        if chapter.is_available():
            li = xbmcgui.ListItem(title, label2=chapter.sub_title)
            url = proxy.video_url(chapter.streaming)
            li.setIconImage(detail.thumbnail)
            xbmcplugin.addDirectoryItem(handle=ctx.addon_handle, listitem=li, url=url)
        else:
            li = xbmcgui.ListItem(u'\u2205 ' + title, label2=chapter.sub_title)
            url = proxy.create_url('not_available', course_id=course_id)
            li.setIconImage(ctx.get_image('lock.png'))
            xbmcplugin.addDirectoryItem(handle=ctx.addon_handle, listitem=li, url=url)

    xbmcplugin.endOfDirectory(ctx.addon_handle)

    win = xbmcgui.getCurrentWindowId()




def not_available(course_id):
    dialog = xbmcgui.Dialog()
    dialog.notification("Not available", "Buy the course in order to have access", icon='OverlayLocked.png')



def educator_detail(educator_id):
    detail = proxy.educator_detail(educator_id)
    _add_courses(detail.courses)




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


func = globals()[ctx.get_func()]
nargs = func.func_code.co_argcount
args = func.func_code.co_varnames[0:nargs]
argValues = [ctx.get_param(arg) for arg in args]
func(*argValues)
