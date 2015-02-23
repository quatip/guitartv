import json
import re
import requests
from .educator import Educator

class TrueFireMock:

    session_params = {}

    def __init__(self, context):
        self.context = context

    def courses(self):
        return self._open_mock('courses_general')['general_courses']

    def course_detail(self, course_id):
        return self._open_mock('courses_detail')

    def available(self):
        return self._open_mock('available')

    def course_description(self, course_id):
        return self._open_mock('course_description_{}'.format(course_id))

    def educators(self):
        return [ Educator(entry) for entry in self._open_mock('educators') ]


    def create_url(self, func, **kwargs):
        return self.context.create_url(func, **kwargs)

    def video_url(self, m3u8url):
        m3u8 = requests.get(m3u8url)
        baseurl = re.match(r'.*/', m3u8.url).group()
        m3u8lines = m3u8.text.split('\n')
        chunklists = [x for x in m3u8lines if re.match(r'^.*m3u8$', x)]
        video = baseurl + chunklists[0]
        return video

    def _open_mock(self, file):
        with open(self.context.get_datafile_path(file)) as data_file:
            return json.load(data_file)
