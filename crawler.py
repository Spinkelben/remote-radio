import requests
from html.parser import HTMLParser
import re
import json


class IndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    if "radio" in attr[1]:
                        match = re.match(r"/radio/(.*)([a-zA-Z]\d+)/$", attr[1])
                        if match is not None:
                            self.ids.add((match.group(1), match.group(2)))

def magic_query(station_ids):
    results = []
    for idx, station_id in enumerate(station_ids):
        print("Station {} of {}".format(idx, len(station_ids)))
        response = requests.get(r"https://opml.radiotime.com/Tune.ashx?id={}&render=json&formats=mp3,aac,ogg,flash,html&partnerId=RadioTime&version=2".format(station_id[1]))
        response = response.json()
        if response['head']['status'] == '200':
            best_url = None
            best_bitrate = 0
            for element in response['body']:
                bitrate = int(element['bitrate'])
                if bitrate > best_bitrate:
                    best_bitrate = bitrate
                    best_url = element['url']
            if best_url is not None:
                results.append((station_id[0], best_url))
    return results

index = requests.get("https://tunein.com/radio/Denmark-r101233/")
parser = IndexParser()
parser.feed(index.text)

print(parser.ids)
print(magic_query(parser.ids))
