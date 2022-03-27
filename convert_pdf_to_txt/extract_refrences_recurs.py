
from distutils import text_file
import json
import pprint
# Write three funtions 
# 2. Loop through the references.txt and check with the json file if matching file found then extract those references

def walk_the_references(ref_path):
    line = []
    txt_file = open(ref_path,'r')
    ref_count = 1
    for i in txt_file:
        if i.startswith('['):
            line.append(i)
            ref_count += 1
        if ref_count >= 7:
            break
    pprint.pprint(line)


def get_title_names():
    json_file = open('title.json')
    data = json.load(json_file)
    # pprint.pprint(data)
    return data





data = get_title_names()
walk_the_references('references/2008Rosten_FasterAndBetterAMachineLearningApproachToCornerDetection.txt')