import os
from os.path import exists
from filehandler import IndexPrinter
from collections import defaultdict
from time import time
import xml.sax
import re
import sys
import time
from itertools import chain
import nltk
from nltk.corpus import stopwords
from Stemmer import Stemmer

# ps = PorterStemmer()
ps = Stemmer('porter')


# xml.sax = Simple API for XML
# in SAX, we never load the full xml file into the RAM, but only pieces we need in the moment
# in DOM - document object model to load entire xml file into RAM and create hierarchical structure

# ---------------------------------------------------------------------------- #
#                             Global Variables                                 #
# ---------------------------------------------------------------------------- #
# nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
# infobox, reflist, can also be added to stopwords?
totalDocumentsParsed = 0
index = defaultdict(list)
title_list = []
# 1500 documents per file
maxDocuments = 15000
filecounter = 0
dirpath = sys.argv[2]
file_exists = exists(dirpath)
if file_exists == False:
    os.mkdir(dirpath)
new_new_folder = "titles"
file_indeed_exists = exists(new_new_folder)
if file_indeed_exists == False:
    os.mkdir(new_new_folder)
# dirpath = "indexfolder/"
st = time.time()
total_tokens = 0
index_tokens = 0

# ---------------------------------------------------------------------------- #
#                             XML Parsing                                      #
# ---------------------------------------------------------------------------- #


class TextProcessing:
    def __init__(self):
        pass

    def tokenise(self, data):
        tokens = re.split(r"[^A-Za-z0-9]+", data)
        global total_tokens
        total_tokens += len(tokens)
        return tokens

    def stemming_and_stopping(self, data):
        StemmedUp = []
        StemmedUp = [ps.stemWord(i) for i in data if i not in stop_words if len(i) < 35 if len(i) >=2]
        
            
        return StemmedUp

    def category_extraction(self, data):
        # tcat = time.time()
        categories = list()
        categories = re.findall(r"\[\[category:(.*)\]\]", data)
        cate = self.tokenise(" ".join(categories))
        # stemming and stopping
        stemmed_tokens = self.stemming_and_stopping(cate)
        # print(stemmed_tokens)
        # quit()
        # print("category extraction time ", time.time() - tcat)
        return stemmed_tokens

    def references_extraction(self, data):
        # tref = time.time()
        reference_list = re.findall(
            r"== ?references ?==(.*?)\n\n", data, flags=re.DOTALL | re.MULTILINE
        )
        reflist = self.tokenise(" ".join(reference_list))
        # stemming
        stemmed_tokens = self.stemming_and_stopping(reflist)
        # print(stemmed_tokens)
        # quit()
        # print("references extraction time ", time.time() - tref)
        return stemmed_tokens

    def body_extraction(self, data):
        # tbod = time.time()
        # references body mein remove symbols pattern
        body_text = re.sub(r"\{\{.*\}\}", r" ", data)
        body_text = self.tokenise(body_text)
        # stemming
        stemmed_tokens = self.stemming_and_stopping(body_text)
        # print(stemmed_tokens)
        # quit()
        # print("body extraction time ", time.time() - tbod)
        return stemmed_tokens

    def links_extraction(self, data):
        tlin = time.time()
        links = re.findall(r"==external links==\n[\s\S]*?\n\n", data)
        links = " ".join(links)
        links = links[20:]
        links = re.sub("[|]", " ", links)
        links = re.sub("[^a-zA-Z ]", " ", links)
        linklist = self.tokenise(links)
        # stemming
        stemmed_tokens = self.stemming_and_stopping(linklist)
        # print(stemmed_tokens)
        # quit()
        # print("links extraction time ", time.time() - tlin)
        return stemmed_tokens

    def infobox_extraction(self, data):  # demoss #
        # tinf = time.time()
        infobox_data = list()
        data = re.split(r"==\s*references\s*==", data)
        # infobox_data = data[0]
        check = data[0].split("{{infobox")
        x = len(check)

        if x <= 1:
            return infobox_data
        else:
            infobox_listing = data[0].split("\n")
            flag = False
            for i in infobox_listing:
                f = re.match(r"\{\{infobox", i)
                if f == False and flag == True:
                    if i == "}}":
                        flag = False
                        continue
                    infobox_data.append(i)
                elif f:
                    flag = True
                    i = re.sub(r"\{\{infobox(.*)", r"\1", i)
                    infobox_data.append(i)
                    

            infobox_data = self.tokenise(" ".join(infobox_data))
            # stemming
            stemmed_tokens = self.stemming_and_stopping(infobox_data)
            # print(stemmed_tokens)
            # quit()
            # print("infobox extraction time ", time.time() - tinf)
            return stemmed_tokens
            # return ''

    def processData(self, data, flag):
        global totalDocumentsParsed
        # case folding
        data = data.lower()
        # if flag is true, return title
        if flag == True:
            # tokenisation
            tokens = self.tokenise(data)
            # print(tokens)
            # get title for storing
            # stemming
            stemmed_tokens = self.stemming_and_stopping(tokens)
            # print("total = ", totalDocumentsParsed)
            # print(stemmed_tokens)
            return stemmed_tokens
        else:
            references = list()
            category = list()
            links = list()
            body = []
            infobox = []
            # removing {|}
            data = re.sub(r"{\|(.*?)\|}", " ", data, flags=re.DOTALL)
            # removing html stuff
            data = re.sub(r"&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;", r" ", data)
            # # need to look at this
            # made changes here
            data = re.sub(r'{{v?cite(.*?)}}', ' ', data, flags=re.DOTALL)
            # # need to look at this
            data = re.sub(r'<(.*?)>', ' ', data, flags=re.DOTALL)

            links = self.links_extraction(data)
            # substituting hyperlinks with " "
            data = re.sub(r"http\S*[\s | \t | \n]", r" ", data)
            references = self.references_extraction(data)
            category = self.category_extraction(data)
            body = self.body_extraction(data)
            infobox = self.infobox_extraction(data)

            return body, infobox, category, links, references


def looper(typo, diction, wording):
    for i in typo:
        diction[i] += 1
        wording[i] += 1

# ---------------------------------------------------------------------------- #
#                             Index Creation                                   #
# ---------------------------------------------------------------------------- #

def index_creator(file_title, title, body, infobox, category, links, references):
    global totalDocumentsParsed
    global index
    global title_list
    global maxDocuments
    num = totalDocumentsParsed
    global filecounter
    global dirpath
    global index_tokens
    words = defaultdict(int)

    b = defaultdict(int)
    t = defaultdict(int)
    c = defaultdict(int)
    inf = defaultdict(int)
    l = defaultdict(int)
    r = defaultdict(int)
    looper(body, b, words)
    looper(title, t, words)
    looper(category, c, words)
    looper(infobox, inf, words)
    looper(links, l, words)
    looper(references, r, words)

    index_type = ["d", "t", "b", "i", "c", "l", "r"]

    for i in words.keys():
        # d for document id/number
        s = index_type[0] + str(num)
        # t for title id
        idtitle = t[i]
        if idtitle:
            s += index_type[1] + str(idtitle)
        # b for body id
        idbody = b[i]
        if idbody:
            s += index_type[2] + str(idbody)
        # i for infobox id
        idinfobox = inf[i]
        if idinfobox:
            s += index_type[3] + str(idinfobox)
        # c for category id
        idcategory = c[i]
        if idcategory:
            s += index_type[4] + str(idcategory)
        # l for link id
        idlink = l[i]
        if idlink:
            s += index_type[5] + str(idlink)
        # r for references id
        idreferences = r[i]
        if idreferences:
            s += index_type[6] + str(idreferences)

        index[i].append(s)
        index_tokens += 1

    if totalDocumentsParsed % maxDocuments == 0:
        title_list, index, filecounter = IndexPrinter(title_list, index, filecounter, dirpath)
        title_list = []
        # print("Made file ",filecounter)


# ---------------------------------------------------------------------------- #
#                             Handler                                          #
# ---------------------------------------------------------------------------- #


class WikiDumpXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current = ""
        self.title = ""
        self.text = ""
        self.processor = TextProcessing()

    # Call when an element starts
    def startElement(self, name, attrs):
        self.current = name

    # Call when a character is read
    def characters(self, content):
        if self.current == "text":
            self.text += content
        elif self.current == "title":
            self.title += content

    # Call when an elements ends
    def endElement(self, x):
        global st
        global title_list
        global totalDocumentsParsed
        if self.current == "title":
            # print(f"title: {self.title}")
            totalDocumentsParsed += 1
            WikiDumpXMLHandler.title_processed = self.processor.processData(
                self.title, True
            )
            title_list.append(self.title)
            
        if self.current == "text":
            # print(f"text: {self.text}")
            body, infobox, category, links, references = self.processor.processData(
                self.text, False
            )
            # next is indexing right here
            index_creator(self.title, WikiDumpXMLHandler.title_processed,
                          body, infobox, category, links, references)
            # if(totalDocumentsParsed == 15000):
            #     et = time.time()
            #     print("time taken = ", et - st)
            #     quit()
            # print(body)
            # body mein issue? theek lag raha hai
            # infobox fixed
            # links not sure
            # categories is ok
            # references seems ok
            # quit()
        # elif self.current == "page":
        #     pass
        # totalDocummentsParsed += 1
        self.current = ""
        self.title = ""
        self.text = ""


# print(totalDocumentsParsed)


# url = "http://www.google.com/"
# data = re.sub(r'http\S*[\s | \t | \n]', r' ', url)
# data = re.sub(r'http[^\ ]*\ ', r' ', url)
# print(data)
# quit()

# ---------------------------------------------------------------------------- #
#                             main                                             #
# ---------------------------------------------------------------------------- #

Handler = WikiDumpXMLHandler()
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
parser.setContentHandler(Handler)
# parser for phase 1:
filepath = sys.argv[1]
parser.parse(filepath)

title_tmp, index, filecounter = IndexPrinter(title_list, index, filecounter, dirpath)
et = time.time()
print("time taken = ", et - st)

# ---------------------------------------------------------------------------- #
#                             token counter                                    #
# ---------------------------------------------------------------------------- #
invertedindex_stats = sys.argv[3]
with open(invertedindex_stats, 'w') as f:
    string = "Total Tokens: " + str(total_tokens) + "\n"
    f.write(string)
    string = "Tokens in inverted index: " + str(index_tokens) + '\n'
    f.write(string)