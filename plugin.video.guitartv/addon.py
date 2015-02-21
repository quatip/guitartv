import re
import requests
import xbmcgui
import xbmcplugin
from resources.lib import truefire
from resources.lib import context

context = context.Context()
provider = truefire.TrueFireProxy(context)

def root():
    courses = provider.courses()

    for c in sorted(courses, key=lambda x: x['title']):
        li = xbmcgui.ListItem(c['title'], iconImage=c['thumbnailURL'])        
        url = context.create_url({'func': 'course_detail', 'course_id': c['id']})
        xbmcplugin.addDirectoryItem(
            handle=context.addon_handle, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(context.addon_handle)


def course_detail(course_id):

    detail = provider.course_detail(course_id)
    course = detail['course']

    for chapter in detail['video_files']:
        if chapter['videoUrl']:
            li = xbmcgui.ListItem(chapter['videoTitle'], label2=chapter['videoSubTitle'])
            li.setArt({'fanart': course['videoPreviewImage']})
            xbmcplugin.addDirectoryItem(handle=context.addon_handle, 
                                        url=provider.video_url(chapter['videoStreamingUrl']), listitem=li)

    xbmcplugin.endOfDirectory(context.addon_handle)


if 'func' in context.params:
    funcname = context.params['func'][0]
    func = globals()[funcname]
    nargs = func.func_code.co_argcount
    args = func.func_code.co_varnames[0:nargs]
    argvalues = [lambda arg: context.params[arg][0] for arg in args]
    func(*argvalues)
else:
    root()
