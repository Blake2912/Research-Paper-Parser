from hashlib import new
import re
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import WordPunctTokenizer
import bs4 as bs
import heapq

user_input=open('RS_2005.txt',encoding="utf-8")
output_file=open('output.txt','w+')
section_extraction=open('output1.txt','w+')
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

def main():
    text=user_input.read()
    line_list = []
    line_list = str(text).split("\n")
    Summary(line_list)
    output_file.close()
    user_input.close()

if __name__ == "__main__":
    main()
