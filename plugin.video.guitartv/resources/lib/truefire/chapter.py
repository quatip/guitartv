class Chapter:
    def __init__(self, json):
        self.url = json['videoUrl']
        self.title = json['videoTitle']
        self.sub_title = json['videoSubTitle']
        self.streaming = json['videoStreamingUrl']

    @staticmethod
    def make(json_array):
        return [Chapter(json) for json in json_array]