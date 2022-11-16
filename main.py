from os import mkdir, walk
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer, util
from FileDetails import FileDetails

import bs4 as bs
import heapq
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import WordPunctTokenizer

import re
import pickle
import json


"""
*****************
  UTIL FUNCTIONS
*****************
"""
def get_file_list_from_folder(folder_name):
    file_list = []
    try:
        for(files) in walk(str(folder_name),topdown=True):
            file_list = files[len(files) - 1]
            # Code for cleaning up the file list remove all files starting with ._
            for i in file_list:
                if i.startswith("._"):
                    file_list.remove(i)
        return file_list
    except:
        raise FileNotFoundError


"""
***************************
  CONVERT PDF TO TXT CODE
***************************
"""
def remove_pdf_extension(string):
    string = str(string)
    string = string.split('.')
    return string[0]

def extract_text1(pdf_name):
    text = extract_text(pdf_name)
    return text

def save_in_txt_files(pdf_path):
    """
    Points to be noted while passing the pdf_name...
        1. The pdf_name is the pdf path like => Repository/pdf_name.pdf
    """
    print(pdf_path)
    path_splits = pdf_path.split("/")
    filepath = str("output/"+remove_pdf_extension(path_splits[len(path_splits)-1])+".txt")
    try:
        file = open(r"{}".format(filepath),"w")
        text = extract_text1(pdf_path)
        text = str(text)
        file.write(text)
        file.close()
        return text
    except:
        mkdir('output')


"""
*************************
    EXTRACT HEADINGS
*************************
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

def extract_heading_in_list(path_to_txt_file):
    with open(path_to_txt_file,"r") as f:
        content = f.read()
        headings = extract_headings(content)
        f.close()
        return headings

def get_headings_from_list(txt_file_list,txt_folder_name):
    heading_frequency_dict = {}
    replaceObject = re.compile(r'^[0-9]\.+\s+')
    for i in txt_file_list:
        heading_list = extract_heading_in_list("{0}/{1}".format(txt_folder_name,i))
        for j in heading_list:
            processed_txt = replaceObject.split(j)
            processed_heading = processed_txt[len(processed_txt) - 1].upper().strip()
            if processed_heading in heading_frequency_dict:
                heading_frequency_dict[processed_heading] += 1
            else:
                heading_frequency_dict[processed_heading] = 1
    print(heading_frequency_dict,end='\n')


"""
********************************************
  EXTRACT REFERENCES AND SAVE IT IN FOLDER
********************************************
"""

def extract_reference_from_txt_file(path_of_txt_file,source_folder_name):
    txt_path = str(source_folder_name+"/"+path_of_txt_file)
    txt_file = open(txt_path,'r')
    ref_int = 0
    references = str("references/"+path_of_txt_file)
    try:
        ref_file = open(r"{}".format(references),"w")
        for i in txt_file:
            if ref_int == 1:
                ref_file.write(i)
            i = i.rstrip()

            if re.search(".*References|.*REFERENCES",i):
                ref_int=1
    except:
        try:
            mkdir('references')
        except:
            print("directory found!")
    txt_file.close()


"""
********************************************
  MATCHING REFERENCES WITH TITLE OF PAPERS
********************************************
"""
# Problem Solution: https://www.sbert.net/docs/usage/semantic_textual_similarity.html
# Sentence Transformet: https://pypi.org/project/sentence-transformers/

heading_find_regex = re.compile(r': [A-Za-z]+ .*')
number_check_regex_type_1 = re.compile(r'[0-9]+\.') # 21.
number_check_regex_type_2 = re.compile(r'\[[0-9]+\]') # [2]

def remove_starting_numbers(input_list):
    temp_list = []
    res_list = []
    temp_list = input_list
    for i in temp_list:
        sentence = i.split(' ')
        if number_check_regex_type_1.search(str(sentence[0])):
            sentence.remove(sentence[0])
            sen = " ".join(sentence)
            res_list.append(sen)
        elif number_check_regex_type_2.search(str(sentence[0])):
            sentence.remove(sentence[0])
            sen = " ".join(sentence)
            res_list.append(sen)
        else:
            res_list.append(sentence)
    
    for i in res_list:
        if i == ['']:
            res_list.remove(i)
    
    return res_list

def search_references(references_list,heading_list,model):
    ref_temp = references_list
    res_list = remove_starting_numbers(ref_temp)
    # search_dict = dict()
    for i in range(len(res_list)):
        encode_i = model.encode(res_list[i],convert_to_tensor=True)
        for j in heading_list:
            cosine_scores = util.cos_sim(encode_i,j['Encoding_data'])
            if cosine_scores[0][0] >= 0.7:
                print("S1:{0} \nS2:{1} \n\tScore: {2}".format(res_list[i],j['Title'],cosine_scores[0][0]))

def extract_references_from_file(file_path):
    sentence_list = []
    main_list = []
    ref_list = []
    match_only_list = []
    temp = ''
    txt_file = open(file_path,'r')
    temp = ''.join(txt_file)
    sentence_list = temp.splitlines(True)

    # Removing extra new-line characters.
    for i in sentence_list:
        if i == '\n':
            sentence_list.remove(i)

    for i in sentence_list:
        search_str = i.split(' ')[0]
        if number_check_regex_type_1.search(str(search_str)):
            # print(i)
            main_list.append((i,'MATCHED'))
            match_only_list.append(i)
            
        elif number_check_regex_type_2.search(str(search_str)):
            main_list.append((i,'MATCHED'))
        else:
            main_list.append((i,'NOT_MATCHED'))
    
    ref = ''
    for i in main_list:
        if i[1] == 'MATCHED':
            ref_list.append(ref)
            ref = i[0]
        else:
            ref += i[0]
    ref_list.append(ref)       
    
    ref_temp = []
    for i in ref_list:
        ref_temp.append(i.replace("\n", "").replace("\x0c",""))
    
    ref_list = ref_temp
    return ref_list
    

def get_title_names(model):
    json_file = open('REFERENCES.json')
    data_array = json.load(json_file)
    file_details_array = []
    for i in data_array:
        title_encode = model.encode(i['Title'],convert_to_tensor=True)
        # print(title_encode)
        file_details = FileDetails(i['Title'],i['Filename'],title_encode)
        file_details_array.append(file_details)
    return file_details_array

# This function should run only once or whenever necessary
def save_headings_to_pickle(model):
    file_details_array = get_title_names(model)
    processed_title = open('PROCESSED_REFERENCES.pkl','wb')
    processed_list = []
    for i in file_details_array:
        processed_list.append({"Title": i.title,"Path": i.path, "Encoding_data": i.encoding_data})
    pickle.dump(processed_list,processed_title)
    processed_title.close()


"""
*********************
  SUMMARY OF PAPERS
*********************
"""

def Summary(line_list):
    heading_list = []
    def TextSummarization(res):
        article = res

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text
        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+',' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')
        
        word_frequencies = {}
        sentence_scores = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())
            
        
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        output_file.write(summary)
        print(summary)
        
    def textExtraction(new_heading,heading_lower):
        c = [x for x in heading_lower if any(k in x for k in new_heading)]
        inverse_index = { element: index for index, element in enumerate(c) }

        #To find the index of the matched elements in the original heading list
        z= [(index) for index, element in enumerate(heading_lower) if element in inverse_index]
        #To extract the text under the sections
        res = ''
        for i in z:
            p=heading_list[i]
            if(p[3:]=="CONCLUSION" or p[3:]=="conclusion" or p[3:]=="Conclusion"):
                j=heading_list[i]
                k="REFERENCES"
            
    # getting index of substrings
                idx1 = line_list.index(j)
                idx2 = line_list.index(k)
                res = ''
    # getting elements in between
                for idx in range(idx1 + 1, idx2):
                    res = res + line_list[idx]
            else:
                j=heading_list[i]
                k=heading_list[i+1]
            # getting index of substrings
                idx1 = line_list.index(j)
                idx2 = line_list.index(k)
                res = ''
            # getting elements in between
                for idx in range(idx1 + 1, idx2):
                    res = res + line_list[idx]
                    print("res",res)
        section_extraction.write(res)
        TextSummarization(res)
    def synonymmatch(crct_heading,heading_list):
        a = (map(lambda x: x.lower(), heading_list))
        heading_lower= list(a)
        synonyms=["abstract","introduction","literature-survey","related work","background","methodology","analysis","comparison","discussion","results","conclusion","references"]
        new_heading=[]
        synonyms.append("CONCLUSIONS")
    #to check and extract the matching headings and synonyms
        for i in synonyms:
            if i in crct_heading:
                new_heading.append(i)
        new_heading=list(set([x for x in crct_heading if any(b in x for b in synonyms)]))
        textExtraction(new_heading,heading_lower)

    def ExtractHeading():
    
    # TO extract the headings
        for i in line_list:
            matchOject = re.compile(r'^[0-9]\.+\s+\w+[\s\w]+')
            temp_heading = matchOject.findall(i)
            if temp_heading != []:
                for i in temp_heading:
                    heading_list.append(i)
        
        crct_heading=[]

    #To find the headings without the section number to match with the synonyms and convert it to lower case
        for i in heading_list:
            matchOject = re.compile(r'\w+[\s\w]+')
            temp_heading = matchOject.findall(i)
            if temp_heading != []:
                for i in temp_heading:
                    crct_heading.append(i)
        for i in range(len(crct_heading)):
            crct_heading[i] = crct_heading[i].lower()
        synonymmatch(crct_heading,heading_list)
    ExtractHeading()


"""
****************
  MAIN FUNCTION
****************
"""
if __name__ == '__main__':
    option = int(input(
        """
        What operation do you want to perform select the appropriate option
            1. To setup the repository, convert the pdf data files to text
            2. To extract headings and display its frequency
            3. To extract references
            4. To find references with title names
            5. To find the summary of the input paper

        Enter the number for performing the given operation:
        """
    ))
    if option == 1:
        folder_name = str(input("Enter the folder name which has the pdf files: "))
        file_list = get_file_list_from_folder(folder_name)
        for pdf_path in file_list:
            save_in_txt_files("{0}/{1}".format(folder_name,pdf_path))

    elif option == 2:
        # NOTE 1: GET YOUR PDF AND TXT FILES SETUP BEFORE RUNNING THIS OPTION
        # NOTE 2: THIS IS A GENERATED FOLDER IT WILL BE GENERATED SO NEED OF CHANGING THE FOLDER NAME
        folder_name = 'output'
        file_list = get_file_list_from_folder(folder_name)
        get_headings_from_list(file_list,folder_name)

    elif option == 3:
        folder_name = 'output'
        file_list = get_file_list_from_folder(folder_name)
        for i in file_list:
            extract_reference_from_txt_file(i,folder_name)

    elif option == 4:
        print("Please wait... searching in our database!")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        a_file = open('PROCESSED_REFERENCES.pkl','rb')
        output = pickle.load(a_file)
        a_file.close()
        reference_list = extract_references_from_file('references/2018Siva_OmnidirectionalMultisensoryPerceptionFusionLongTermPlaceRecognition.txt')
        search_references(reference_list,output,model)
    
    elif option==5:
        user_input=open('RS_2005.txt',encoding="utf-8")
        output_file=open('output.txt','w+')
        section_extraction=open('output1.txt','w+')
        text=user_input.read()
        line_list = []
        line_list = str(text).split("\n")
        Summary(line_list)
        output_file.close()
        user_input.close()

        
