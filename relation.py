# -*- coding: utf-8 -*-
import json

def paper_index_term(fileName):
    """ Output a file contains relation between paper and index_terms_1(first layer of classws)"""

    #build index_term dictionary
    index_term_1 = {}
    with open("index_term_1998_1.txt", encoding='utf-8') as index_file:
        for line in index_file:
            list = line.strip().split('\t')
            index_term_1[list[1]] = list[0] # word: index_number
    print(index_term_1)

    with open(fileName,encoding='utf-8') as data_file:
        count = 1 # sample counter
        result_file = open("paper-index_term.txt",'wt', encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            if "index_term" in data:
                index_term = data["index_term"].strip()

                # match
                for k in index_term_1:
                    if index_term.lower() == k.lower():
                        result_file.write(str(count)+'\t' + str(index_term_1[k]) + '\n' )
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1
