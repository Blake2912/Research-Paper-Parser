import pickle
import json
from FileDetails import FileDetails
import re
from sentence_transformers import SentenceTransformer, util

# Problem Solution: https://www.sbert.net/docs/usage/semantic_textual_similarity.html
# Sentence Transformet: https://pypi.org/project/sentence-transformers/


heading_find_regex = re.compile(r': [A-Za-z]+ .*')
number_check_regex_type_1 = re.compile(r'[0-9]+\.') # 21.
number_check_regex_type_2 = re.compile(r'\[[0-9]+\]') # [2]

model = SentenceTransformer('all-MiniLM-L6-v2')

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

def search_references(references_list,heading_list):
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
    

def get_title_names():
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
def save_headings_to_pickle():
    file_details_array = get_title_names()
    processed_title = open('PROCESSED_REFERENCES.pkl','wb')
    processed_list = []
    for i in file_details_array:
        processed_list.append({"Title": i.title,"Path": i.path, "Encoding_data": i.encoding_data})
    pickle.dump(processed_list,processed_title)
    processed_title.close()

a_file = open('PROCESSED_REFERENCES.pkl','rb')
output = pickle.load(a_file)
a_file.close()
# print(output)


reference_list = extract_references_from_file('references/2018Siva_OmnidirectionalMultisensoryPerceptionFusionLongTermPlaceRecognition.txt')
# reference_list = extract_references_from_file('references/2005Mozos_LearningOfPlacesUsingAdaboost.txt')
search_references(reference_list,output)
# extract_references_from_file('references/2018Siva_OmnidirectionalMultisensoryPerceptionFusionLongTermPlaceRecognition.txt')
# CMRIT-COE/convert_pdf_to_txt/references/2005Mozos_LearningOfPlacesUsingAdaboost.txt
