import json


class JsonReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get_test_data(self, key):
        data = self.read_json()
        return data.get(key)