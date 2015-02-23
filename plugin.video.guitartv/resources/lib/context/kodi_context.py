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
        self.addon = xbmcaddon.Addon()

    def get_func(self):
        return self.get_param('func') or 'root'

    def get_param(self, param):
        if param in self.params:
            return self.params[param][0]
        else:
            return None

    def get_datafile_path(self, filename):
        return xbmc.translatePath(
            self.addon.getAddonInfo('path') + '/resources/data/' + filename + '.json')

    def create_url(self, funcname, **kwargs):
        kwargs['func'] = funcname
        url = self.url + '?' + urllib.urlencode(kwargs)
        #print "URL: {}".format(url)
        return url

