import json
import requests


class WebProvider:
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

    def query(self, command, **kwargs):
        kwargs['auth_token'] = self.auth_token
        answer = requests.get(self.api_url + '/' + command, params=kwargs).json()
        self._save_mock(answer, command, **kwargs)
        return answer

    def _save_mock(self, j_object, command, **kwargs):
        filename = self.context.get_datafile_path(command, **kwargs)
        with open(filename, 'w') as outfile:
            json.dump(j_object, outfile)
