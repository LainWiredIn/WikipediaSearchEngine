from collections import defaultdict
import sys
import os
import math
from math import log2
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from Stemmer import Stemmer
import random
import time
from bisect import bisect
# for keeping list sorted

ps = Stemmer('porter')
stop_words = set(stopwords.words('english'))
secondary_main_file = open('secondary/sindex_main.txt', 'r')
secondary_main = secondary_main_file.readlines()
secondary_main_file.close()


first_clue = 1
second_clue = 1

no_of_terms = 480000
# 316 x 1500

# support for field queries
fieldtypes = ['t', 'b', 'r', 'c', 'l', 'i']
fieldscores = [50, 10, 8, 8, 8, 28]
fieldmap = {'t':0, 'b':1, 'r':2, 'c':3, 'l':4, 'i':5}

def preprocessing(data):
    data = data.lower()
    # removing {|}
    data = re.sub(r"{\|(.*?)\|}", " ", data, flags=re.DOTALL)
    data = re.sub(r"&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;", r" ", data)
    # substituting hyperlinks with " "
    data = re.sub(r"http\S*[\s | \t | \n]", r" ", data)
    # data = re.sub(r'<(.*?)>', ' ', data, flags=re.DOTALL)
    tokens = re.split(r"[^A-Za-z0-9]+", data)
    StemmedUp = []
    StemmedUp = [ps.stemWord(i) for i in tokens if i not in stop_words if len(i) < 35 if len(i) >=2]
    return StemmedUp

def get_pl(data):
    appended_token = data + '\n'
    pos = bisect(secondary_main, appended_token)
    pos = pos - 1
    
    if pos >= 0:
        str_pos = str(pos)
        file = open('secondary/sindex' + str_pos + '.txt', 'r')
        # print(str_pos)
        line = file.readline().strip()
        while line:
            var1 = line.split(':')[0]
            if(var1 == data):
                # print(line.split(':')[1])
                var = line.split(':')[1]
                return var
            line = file.readline().strip()
    return False

def title_extractor(data, max):
    # floor division
    off = math.floor(data/max)
    file = open('titles/' + str(off) + '.txt', 'r')

    title = file.readlines()[data % max-1].strip()
    return title

def plain_query(line):
    global first_clue
    global second_clue
    global no_of_terms
    minimizer = 10
    stringer = list()
    score = defaultdict(int)
    tokens = preprocessing(line)
    for token in tokens:
        # print(token)
        pl = get_pl(token)
        if pl:
            document_list = re.split('d', pl)[1:]
            # print(document_list)
            df = len(document_list)
            print(df)
            # computing inverse document frequency
            idf = log2(no_of_terms/df)
            token_count = defaultdict(int)
            for doc in document_list:
                # if first_clue == 1:
                    # print(doc)
                pageid = ''
                for i in doc:
                    if i!='0' and i!='1' and i!='2' and i!='3' and i!='4' and i!='5' and i!='6' and i!='7' and i!='8' and i!='9':
                        break
                    else:
                        pageid = pageid + i
                if first_clue == 1:
                    first_clue = 0
                    # print(pageid)
                pageid = int(pageid)
                temp_list = []
                for i in range(6):
                    tmp = doc.find(fieldtypes[i])
                    # if(pageid==91):
                    #     print(tmp)
                    if tmp<=0 :
                        temp_list.append(0)
                    else:
                        x=0
                        y=1
                        ii=tmp+1
                        while(ii<len(doc)and doc[ii]<='9' and doc[ii]>='0'):
                            x*=10
                            x+=int(doc[ii])
                            ii+=1
                         
                        temp_list.append(x)
                        # temp_list.append(int(doc[tmp+1]))
                scores = temp_list
                
                for i in range(len(scores)):
                    scores[i] = scores[i]*fieldscores[i]
             
                for s in scores:
                    token_count[pageid] = s + token_count[pageid]
                score[pageid] = log2(token_count[pageid]) * idf + score[pageid]
    final = sorted(score.items(), key=lambda x: x[1], reverse = True)
    # if second_clue == ?1:
        # print(final)
        # second_clue = 0
    # print("finalllll"+str( len(score)))

    for i in range(0, min(minimizer, len(final))):
        stringer.append(str(final[i][0]) + ',' + title_extractor(final[i][0], 15000) + '\n')
    if minimizer > len(final):
        ranger = minimizer - len(final)
        for i in range (ranger):
            randome = random.randint(0, no_of_terms)
            title = title_extractor(randome, 15000)
            stringer.append(str(randome) + "," + title + '\n')
    return stringer
    
def field_query(line):
    global no_of_terms
    minimizer = 10
    stringer = list()
    parsed = defaultdict(int)
    score = defaultdict(int)
    parse_list = []
    line = line.split(':')
    first = 0
    for i in range(len(line)):
        if first:
            splitter = line[i-1].split()
            # print(split_list)
            parse_list.append((splitter[len(splitter) - 1], preprocessing(' '.join(line[i].split()))))
        else:
            first = 1
            
    for i in range(len(parse_list)):
        for token_remember in parse_list[i][1]:
            parsed[token_remember] = parse_list[i][0]
    
    for token in parsed.keys():
        posting_list = get_pl(token)
        if posting_list:
            document_list = re.split('d', posting_list)[1:]
            df = len(document_list)
            # computing inverse document frequency
            idf = log2(no_of_terms/df)
            token_count = defaultdict(int)
            for doc in document_list:
                pageid = ''
                for i in doc:
                    if i!='0' and i!='1' and i!='2' and i!='3' and i!='4' and i!='5' and i!='6' and i!='7' and i!='8' and i!='9':
                        break
                    else:
                        pageid = pageid + i
                pageid = int(pageid)
                # getting document id
                temp_list = []
                for i in range(6):
                    tmp = doc.find(fieldtypes[i])
                    if tmp <= 0:
                        temp_list.append(0)
                    else:
                        x = 0
                        y = 1
                        ii = tmp + 1
                        while(ii<len(doc)and doc[ii]<='9' and doc[ii]>='0'):
                            x *= 10
                            x += int(doc[ii])
                            ii += 1
                         
                        temp_list.append(x)
                        # temp_list.append(int(doc[tmp+1]))
                           
                scores = temp_list
                for i in range(len(scores)):
                    scores[i] = scores[i]*fieldscores[i]
                scores[fieldmap[parsed[token_remember]]] = scores[fieldmap[parsed[token_remember]]]*15000
                for tmp_score in scores:
                    token_count[pageid] = tmp_score + token_count[pageid]
                score[pageid] = log2(token_count[pageid]) * idf + score[pageid]
                
    final = sorted(score.items(), key=lambda x: x[1], reverse = True)
    
    for i in range(0, min(minimizer, len(final))):
        stringer.append(str(final[i][0]) + ',' + title_extractor(final[i][0], 15000) + '\n')
    if minimizer > len(final):
        ranger = minimizer - len(final)
        for i in range (ranger):
            randome = random.randint(0, no_of_terms)
            stringer.append(str(randome) + "," + title_extractor(final[i][0], 15000) + '\n')
    return stringer

def search(line):
    stringer = []
    if re.match(r'[t|b|i|c|l|r]:', line):
        print("this is a field query")
        stringer = field_query(line)
    else:
        print("this is a plain query")
        stringer = plain_query(line)
    return stringer

filename = sys.argv[1]
queryfile = open(filename, 'r')

lines = queryfile.readlines()
queryfile.close()

stringer = []
print(len(lines))
query_op = sys.argv[2]
query_opfile = open(query_op, 'w')

for line in lines:
    st = time.time()
    print("searching for " + line)
    stringer = search(line)
    # stringer+="\n"
    

    et = time.time()
    stringer.append(str(et-st)+'\n\n')
    query_opfile.writelines(stringer )

query_opfile.close()
    
    




