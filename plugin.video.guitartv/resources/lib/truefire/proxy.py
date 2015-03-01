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

    def available(self):
        answer = self.provider.query('user/availablecourses')
        return self.courses_dict()[answer['result']]

    def recently_added(self):
        answer = self.provider.query('courses/recently_added.json?count=25')
        c_dict = self.courses_dict()
        return [c_dict[course['id']] for course in answer['result']]

    def whats_hot(self):
        answer = self.provider.query('courses/whats_hot.json?randomize=1')
        c_dict = self.courses_dict()
        return [c_dict[course['id']] for course in answer['result']]

    def course_description(self, course_id):
        answer = self.provider.query('courses/detail.json/' + str(course_id))
        return Course(answer['course'])

    def educators(self):
        answer = self.provider.query('educator/general.json')
        return Educator.make(answer['result'])

    def educator_detail(self, educator_id):
        answer = self.provider.query('educator/detail.json/' + str(educator_id))
        educator = Educator(answer['result'])
        c_dict = self.courses_dict()
        educator.courses = [c_dict[cid] for cid in answer['result']['publishedCourses'] if c_dict.get(cid)]
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
