
class Educator:
    def __init__(self, json):
        if json.get('educatorName'):
            self.name = json['educatorName']
            self.bio = json['bio']
        else:
            first_name = json['first_name'].strip()
            last_name = json['last_name'].strip()
            self.name = first_name + ' ' + last_name if first_name else last_name
            self.bio = None

        self.thumbnail = json['thumbnail']
        self.id = json['id']
        self.courses = None
        self.fan_art = None


    @staticmethod
    def make(json_array):
        return [Educator(json) for json in json_array]