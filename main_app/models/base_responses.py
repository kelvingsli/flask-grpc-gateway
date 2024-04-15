import json

class BaseResponse(object):

    def __init__(self, response_data=None, error=None):
        self.response_data = response_data
        self.error = error
    

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
