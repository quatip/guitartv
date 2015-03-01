import datetime
import re
from .chapter import Chapter


class Course:
    def __init__(self, course, chapters = None):
        self.id = course['id']
        self.title = course.get('title')

        self.release_date = None
        if course.get('release_date'):
            r_date = course['release_date']
            if re.search(r'(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)', r_date):
                self.release_date = datetime.datetime.strptime(r_date, "%Y-%m-%d %H:%M:%S").date()

        self.duration = None
        if course.get('totalRunningTime'):
            running_time = re.search(r'(\d\d):(\d\d)', course['totalRunningTime'])
            if running_time:
                self.duration = int(running_time.group(1))*60 + int(running_time.group(2))

        self.overview = course.get('overview')
        self.thumbnail = course.get('thumbnailURL')
        self.author_id = course.get('AuthorID')

        if course.get('videoPreviewImage'):
            self.fan_art = course['videoPreviewImage']
        else:
            self.fan_art = 'http://truefire.com/images/courses/{}/169.jpg'.format(self.id)

        self.author = None

        if chapters:
            self.chapters = Chapter.make(chapters)

    @staticmethod
    def make(info_array):
        return [Course(info) for info in info_array]