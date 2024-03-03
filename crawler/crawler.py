import json
import random


class Crawler:
    def __init__(self):
        pass

    def execute_crawler(self, subject,scholar_id, time=0): # needed data will be import as a parameter
        # if subject == "department":
            #execute department crawler
        #if subject == "journal":
            #execute journal crawler
            #when you get the data add traceid to the data
        json_files = ['crawler/empty.json', 'output_test.json']
        chosen_json = random.choice(json_files)
        with open(chosen_json, "r", encoding="utf-16") as file:
                output = json.load(file)
        while not output and time != 2:
            chosen_json = random.choice(json_files)
            with open(chosen_json, "r", encoding="utf-16") as file:
                output = json.load(file)
            time +=1
        return [time, len(output), scholar_id]
