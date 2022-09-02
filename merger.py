# program to create primary index by merging all inverted index files created in phase 1

import heapq
from operator import index
from re import L
import sys
import os
from os.path import exists
import sys
import time
THRESH_MAX = 15000

def primary_index_creation(file_count, dirpath):
    
    heap = []
    files = {}
    words = {}
    pointer = {}
    stringer = ''
    flag = [0] * file_count
    for i in range(file_count):
        filename = dirpath + '/index' + str(i) + '.txt'
        files[i] = open(filename, 'r')
        # print(filename)
        pointer[i] = files[i].readline()
        # strip to remove newline
        flag[i] = 1
        words[i] = pointer[i].split(':')
        # tokenise
        if words[i][0] not in heap:
            heapq.heappush(heap, words[i][0])
    
    count = 0
    close = 0
    primary_file = open('primary/pindex.txt', 'w')
    while any(flag) == 1:
        # print(close)
        temp = heapq.heappop(heap)
        stringer = ''
        count  = count + 1
        for i in range(file_count):
            if flag[i]:
                if words[i][0] == temp:
                    stringer += " "
                    stringer += str(words[i][1].strip())
                    x = files[i].readline()
                    pointer[i] = x
                    pointer[i]=pointer[i].strip()
                    # print(x)
                    if x == "":
                        flag[i] = 0
                        files[i].close()
                        close = close + 1
                    else:
                        words[i] = pointer[i].split(':')
                        if words[i][0] not in heap:
                            heapq.heappush(heap, words[i][0])
                            
        final_string = str(temp) + str(':') + str(stringer) + '\n'
        primary_file.write(final_string)
        # primary_file.close()
                            
                            
def secondary_index_creation(file_count, dirpath):
    primary_read_file = open('primary/pindex.txt', 'r')
    secondary_file = open('secondary/sindex_main.txt', 'w')
    lines = []
    filecount = 0
    threshold = THRESH_MAX
    line = primary_read_file.readline().strip('\n')
    while line:
        # w = line.split(':')
        words = line.split(':')
        word = words[0]
        if not(len(word)>10 and word[0:7].isdecimal()):
            lines.append(line)
        leng = len(lines)
        if(leng == threshold and lines != []):
            word = lines[0].split(':')
            word = word[0] + "\n"
            secondary_file.write(word)
            filename = dirpath + '/sindex' + str(filecount) + '.txt'
            indexed = open(filename, 'w')
            for l in lines:
                indexed.write(l+'\n')
            lines = []
            filecount = filecount + 1
        line = primary_read_file.readline().strip()
                
    if(lines != []):
        word = lines[0].split(':')
        word = word[0] + "\n"
        secondary_file.write(word)
        filename = dirpath + '/sindex' + str(filecount) + '.txt'
        indexed = open(filename, 'w')
        for l in lines:
                indexed.write(l+'\n')
        lines = []
        filecount = filecount + 1
    secondary_file.close()
    primary_read_file.close()
    
        
st = time.time()
DIR = sys.argv[1]

new_folder = "primary"
file_exists = exists(new_folder)
if file_exists == False:
    os.mkdir(new_folder)

new_new_folder = "secondary"
file_indeed_exists = exists(new_new_folder)
if file_indeed_exists == False:
    os.mkdir(new_new_folder)

onlyfiles = next(os.walk(DIR))[2]
file_count = len(onlyfiles)
# print(file_count)
primary_index_creation(file_count, DIR)
secondary_index_creation(file_count, new_new_folder)
et = time.time()
t = et - st
print("time taken: ", t, " seconds")



        



    