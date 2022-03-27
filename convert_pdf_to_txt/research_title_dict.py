import json
import os

"""
This peice of code is for testing purpose, the code will search the 
"""
def walk_through_references(folder_name):
    file_list = []
    file_list_dict = {}
    try:
        for(files) in os.walk(str(folder_name),topdown=True):
            file_list = files[len(files) - 1]
        for i in file_list:
            req_text = i.split('.')
            if req_text[0] in file_list_dict.keys():
                continue
            file_list_dict[req_text[0]] = '{0}/{1}'.format(files[0],i)
        return file_list_dict
    except:
        raise FileNotFoundError


get_ref = walk_through_references('references')

with open('title.json','w') as outjson:
    json.dump(get_ref,outjson)