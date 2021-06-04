import requests
import json
import re

API_KEY = "tUsxS-TrJ2pB"
PROJECT_TOKEN = "tTTNTwG7H25d"
RUN_TOKEN = "tr_aiYL2OAz6"

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {"api_key": self.api_key}
        self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key":API_KEY})
        self.data = json.loads(response.text)
        return self.data

    def get_zero_value(self):
        return "0"

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']
        return "0"

    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']
        return "0"

    def get_total_recoverd(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']
        return "0"

    def get_all_country_names(self):
        data = self.data['country']
        country_list = []
        for i in self.data['country']:
            country_list.append(i['name'].lower())
        return country_list

    def get_specific_country_data(self, location):
        data = self.data['country']
        for content in data:
             if location.lower() == content['name'].lower():
                 return content
        return "0"

data = Data(API_KEY, PROJECT_TOKEN)
# print(data.get_data())