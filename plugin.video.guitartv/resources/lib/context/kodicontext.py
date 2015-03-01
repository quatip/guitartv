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

    def get_datafile_path(self, command, **kwargs):
        command = command.replace('/', '_')
        command = command.replace('?', '_')
        file_name = command if command.endswith('.json') else command + '.json'

        return xbmc.translatePath(
            self.addon.getAddonInfo('path') + '/resources/data/' + file_name)

    def create_url(self, func_name, **kwargs):
        kwargs['func'] = func_name
        url = self.url + '?' + urllib.urlencode(kwargs)
        # print "URL: {}".format(url)
        return url

