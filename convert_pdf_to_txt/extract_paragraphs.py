from os import path
import re
"""
My idea is to get the text which is between the headings extracted like
    Heading1
        Text Text
    Heading2
So give the heading as the argument and return the text that is there in between two paragraphs

IMPORTANT GIVE THE ABSOLUTE PATH FOR THE FILE
"""

"""
************ IN PROGRESS ****************
********* DO NOT RUN THIS CODE **********
"""

def extract_headings(text):
    """
        This function will find any headings in the text file. The regular expression finds the
    string with a number at the start following a period, following a space, following a alphanumberic characters

    Args: String - text
    Return: List(String)
    """
    line_list = []
    heading_list = []
    line_list = str(text).split("\n")
    for i in line_list:
        matchOject = re.compile(r'^[0-9]\.+\s+\w+[\s\w]+')
        temp_heading = matchOject.findall(i)
        if temp_heading != []:
            for i in temp_heading:
                heading_list.append(i)
    return heading_list

def getParagraphs(text_file):
    file = open(str(text_file),"r")
    lines = file.read().split("\n")
    headings = get_headings(text_file)
    for i in lines:
        print(lines)


def get_headings(file_path):
    file = open(str(file_path),"r")
    headings = extract_headings(file.read())
    return headings

path_file = 'output/research_paper1.txt'
getParagraphs(path_file)
# getParagraphs('','','/Users/kcvarun/Documents/NLP_tasks/CMRIT-COE/convert_pdf_to_txt/output/research_paper1.txt')
