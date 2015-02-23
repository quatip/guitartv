import re
import json
import requests
from .educator import Educator

class TrueFireProxy:

    api_url = "https://api.truefire.com/v1"
    res_uri = "http://www.truefire.com"

    def __init__(self, context):
        self.context = context

        if 'auth_token' in context.params:
            self.auth_token = context.params['auth_token'][0]
            self.user_id = context.params['user_id'][0]
        else:
            self._login()

    def _login(self):
        params = {
            'username': self.context.addon.getSetting('username'),
            'pass': self.context.addon.getSetting('password')}

        login = requests.get(self.api_url + "/login", params=params).json()
        self.auth_token = login['token']
        self.user_id = login['member']['id']

    def create_url(self, func, **kwargs):
        return self.context.create_url(func, auth_token=self.auth_token, user_id=self.user_id, **kwargs)

    def courses(self):
        answer = self._get('courses/general.json')['general_courses']
        # self._save_mock('courses_general.json', answer)
        return answer

    def available(self):
        answer = self._get('user/availablecourses')['result']
        self._save_mock('available', answer)
        return answer

    def course_description(self, course_id):
        answer = self._get('courses/detail.json/' + str(course_id), videos=0)['course']
        self._save_mock('course_description_{}'.format(course_id), answer)
        return answer

    def educators(self):
        answer = self._get('educator/general.json')['result']
        #self._save_mock('educators', answer)
        return [ Educator(entry) for entry in answer ]

    def course_detail(self, course_id):
        answer = self._get('courses/detail.json/' + str(course_id), videos=1)
        #self._save_mock('courses_detail', answer)
        return answer

    def video_url(self, m3u8url):
        m3u8 = requests.get(m3u8url)
        baseurl = re.match(r'.*/', m3u8.url).group()
        m3u8lines = m3u8.text.split('\n')
        chunklists = [x for x in m3u8lines if re.match(r'^.*m3u8$', x)]

        if chunklists:
            video = baseurl + chunklists[0]
            return video
        else:
            print "Warning: empty chunklist for {}".format(m3u8.url)
            return None

    def _get(self, command, **kwargs):
        kwargs['auth_token'] = self.auth_token
        answer = requests.get(self.api_url + '/' + command, params=kwargs)
        return answer.json()

    def _save_mock(self, name, jobject):
        filename = self.context.get_datafile_path(name)
        with open(filename, 'w') as outfile:
            json.dump(jobject, outfile)
