import json
import requests


class TrueFireProxy:

    api_url = "https://api.truefire.com/v1"
    res_uri = "http://www.truefire.com"

    def __init__(self, context):
        self.context = context
        if 'auth_token' in context.params:
            auth_token = context.params['auth_token'][0]
            user_id = context.params['user_id'][0]
            self.session_params = {
                'auth_token': auth_token, 'user_id': user_id}
        else:
            self._login()

    def _login(self):
        params = {
            'username': self.context.get_setting('username'),
            'pass': self.context.get_setting('password')}

        login = requests.get(self.api_url + "/login", params=params).json()
        self.session_params = {
            'auth_token': login['token'], 'user_id': login['member']['id']}

    def courses(self):
        answer = self._get('courses/general.json')['general_courses']
        # self._save_mock('courses_general.json', answer)
        return answer

    def course_detail(self, course_id):
        answer = self._get('courses/detail.json/' + course_id, {'videos': 1})
        self._save_mock('courses_detail.json', answer)
        return answer

    def _get(self, command, args={}):
        args['auth_token'] = self.session_params['auth_token']
        answer = requests.get(self.api_url + '/' + command, params=args)
        return answer.json()

    def _save_mock(self, name, jobject):
        filename = self.context.get_datafile_path(name)
        with open(filename, 'w') as outfile:
            json.dump(jobject, outfile)
