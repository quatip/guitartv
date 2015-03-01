import json
import requests


class MockProvider:

    api_url = "https://api.truefire.com/v1"
    res_uri = "http://www.truefire.com"

    def __init__(self, context):
        self.context = context

    def create_url(self, func, **kwargs):
        return self.context.create_url(func, **kwargs)

    def query(self, command, **kwargs):
        with open(self.context.get_datafile_path(command, **kwargs)) as data_file:
            return json.load(data_file)

