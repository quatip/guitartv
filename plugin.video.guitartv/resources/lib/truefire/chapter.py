class Chapter:
    def __init__(self, json):
        self.url = json['videoUrl']
        self.title = json['videoTitle']
        self.sub_title = json['videoSubTitle']
        self.streaming = json['videoStreamingUrl']
        self.owned = json['ownsCourse']
        self.free = json['free'] == 1

    @staticmethod
    def make(json_array):
        return [Chapter(json) for json in json_array]

    def is_available(self):
        return self.free or self.owned