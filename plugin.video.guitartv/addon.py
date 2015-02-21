import re
import requests
import xbmcgui
import xbmcplugin
from resources.lib import truefire
from resources.lib import context

context = context.Context()
xbmcplugin.setContent(context.addon_handle, 'movies')
provider = truefire.TrueFireProxy(context)

def root():
    courses = provider.courses()

    for c in sorted(courses, key=lambda x: x['title']):
        li = xbmcgui.ListItem(c['title'], iconImage=c['thumbnailURL'])        
        url = provider.create_url('course_detail', course_id=c['id'])

        xbmcplugin.addDirectoryItem(
            handle=context.addon_handle, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(context.addon_handle)


def course_detail(course_id):
    detail = provider.course_detail(course_id)
    print detail
    course = detail['course']

    for chapter in detail['video_files']:
        if chapter['videoUrl']:
            li = xbmcgui.ListItem(chapter['videoTitle'], label2=chapter['videoSubTitle'])
            li.setArt({'fanart': course['videoPreviewImage']})
            xbmcplugin.addDirectoryItem(handle=context.addon_handle, 
                                        url=provider.video_url(chapter['videoStreamingUrl']), listitem=li)

    xbmcplugin.endOfDirectory(context.addon_handle)


func = globals()[context.get_func()]
nargs = func.func_code.co_argcount
args = func.func_code.co_varnames[0:nargs]
argvalues = [context.get_param(arg) for arg in args]
func(*argvalues)
