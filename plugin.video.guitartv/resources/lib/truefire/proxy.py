import re
import requests
from .educator import Educator
from .course import Course
from .webprovider import WebProvider


class Proxy:

    api_url = "https://api.truefire.com/v1"
    res_uri = "http://www.truefire.com"
    __courses_dict = None

    def __init__(self, context):
        self.provider = WebProvider(context)

    def create_url(self, func, **kwargs):
        return self.provider.create_url(func, **kwargs)

    def courses(self):
        return self.courses_dict().values()

    def courses_dict(self):
        if Proxy.__courses_dict is None:
            answer = self.provider.query('courses/general.json')
            courses = Course.make(answer['general_courses'])
            Proxy.__courses_dict = dict([(c.id, c) for c in courses])

        return Proxy.__courses_dict

    def get_courses(self, id_list):
        c_dict = self.courses_dict()
        if type(id_list) is int:
            id_list = [id_list]
        return [c_dict[course_id] for course_id in id_list if c_dict.get(course_id)]

    def available(self):
        answer = self.provider.query('user/availablecourses')
        return self.get_courses(answer['result'])

    def recently_added(self):
        answer = self.provider.query('courses/recently_added.json?count=25')
        return self.get_courses([c['id'] for c in answer['result']])

    def whats_hot(self):
        answer = self.provider.query('courses/whats_hot.json?randomize=1')
        return self.get_courses([c['id'] for c in answer['result']])

    def course_description(self, course_id):
        answer = self.provider.query('courses/detail.json/' + str(course_id))
        return Course(answer['course'])

    def educators(self):
        answer = self.provider.query('educator/general.json')
        return Educator.make(answer['result'])

    def educator_detail(self, educator_id):
        answer = self.provider.query('educator/detail.json/' + str(educator_id))
        educator = Educator(answer['result'])
        educator.courses = self.get_courses(answer['result']['publishedCourses'])
        return educator

    def course_detail(self, course_id):
        answer = self.provider.query('courses/detail.json/' + str(course_id), videos=1)
        return Course(answer['course'], answer['video_files'])

    def video_url(self, m3u8url):
        m3u8 = requests.get(m3u8url)
        base_url = re.match(r'.*/', m3u8.url).group()
        m3u8lines = m3u8.text.split('\n')
        chunk_lists = [x for x in m3u8lines if re.match(r'^.*m3u8$', x)]

        if chunk_lists:
            video = base_url + chunk_lists[0]
            return video
        else:
            print "Warning: empty chunklist for {}".format(m3u8.url)
            return None
