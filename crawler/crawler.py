import json
import random


class Crawler:
    def __init__(self):
        pass

    def execute_crawler(self, scholar_id, time=0):
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
