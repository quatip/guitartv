import urllib
import urlparse
import sys
import xbmc
import xbmcaddon
import xbmcplugin


class KodiContext:

    def __init__(self):
        self.url = sys.argv[0]
        self.addon_handle = int(sys.argv[1])
        self.params = urlparse.parse_qs(sys.argv[2][1:])
        self._addon = xbmcaddon.Addon()
        xbmcplugin.setContent(self.addon_handle, 'movies')

    def get_datafile_path(self, filename):
        return xbmc.translatePath(
            self._addon.getAddonInfo('path') + '/resources/data/' + filename)

    def create_url(self, funcname, params={}):
        params['func'] = funcname
        return self.url + '?' + urllib.urlencode(params)

    def get_setting(self, name):
        return self._addon.getSetting(name)
