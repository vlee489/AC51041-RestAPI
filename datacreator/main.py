"""Creates descriptions as filler data"""

import random
import subprocess
from markov import Markov
from os import walk
import re
import json

tags = [
    "splatoon", "esports", "lans", "tournament", "iplSplatoon", "online", "low level", "highlights", "twitch", "stream",
    "super major"
]

categories_counter = {}

film_path = "path/to/films"
filenames = next(walk(film_path), (None, None, []))[2]
file_ = open('jeeves.txt')
markov = Markov(file_)
re_match = re.compile("([a-zA-Z_]+)([0-9]+)")
json_out = []

for vid in filenames:
    if vid.endswith(".mp4"):
        print(vid)
        res = re_match.match(vid).groups()
        if res[0] not in categories_counter:
            categories_counter[res[0]] = 1
        else:
            categories_counter[res[0]] += 1

        json_out.append({
            "name": f"{res[0]} highlight {categories_counter[res[0]]}".replace("_", " "),
            "tags": [random.choice(tags) for x in range(2)],
            "categories": [res[0]],
            "file_location": {
                "provider": "DO",
                "region": "FRA1",
                "file_path": f"movie/storage/path/{vid}"
            },
            "thumbnail_location": {
                "provider": "DO",
                "region": "FRA1",
                "file_path": f"img/storage/path/imgs/{res[0]}{categories_counter[res[0]]}.jpg"
            },
            "description": markov.generate_markov_text(30),
            "tag_line": markov.generate_markov_text(9)
        })
        subprocess.call(['ffmpeg', '-i', f"{film_path}/{vid}", '-ss', '00:05.000', '-vframes', '1',
                         f"/img/working/output/{res[0]}{categories_counter[res[0]]}.jpg"])
print(json_out)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_out, f, ensure_ascii=False, indent=4)
