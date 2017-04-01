# -*- coding: utf-8 -*-
import json
import re
from get_attribute import * # from get_attribute.py file
from collections import OrderedDict

def paper_index_term(fileName):
    """ Output a file contains relation between paper and index_terms_1(first layer of classws)"""

    #build index_term dictionary, key: index term, value: index number
    index_dic = {}
    with open("index_term_1998_1.txt", encoding='utf-8') as index_file:
        for line in index_file:
            list = line.strip().split('\t')
            index_dic[list[1]] = list[0] # word: index_number
    print(index_dic)

    with open(fileName,encoding='utf-8') as data_file:
        count = 1 # sample counter
        result_file = open("paper-index_term.txt",'wt', encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            if "index_term" in data:
                index_term = data["index_term"].strip()

                # match
                result_file.write(str(count)+'\t' + str(index_dic.get(index_term)) + '\n' )
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1


def paper_author(fileName):
    """ Build a relationship file between each paper and their authors, use mark number in author.txt file
    Input is the orginial data file contains this relation."""
    # build index_term dictionary, key: author name value: mark number
    author_dic = {}
    with open("author.txt", encoding='utf-8') as author_file:
        for line in author_file:
            list = line.strip().split('\t')
            author_dic[list[1]] = list[0] # author : mark number
    print(author_dic)

    with open(fileName, encoding='utf-8') as data_file:
        count = 1 #sample counter
        result_file= open("paper-author.txt",'wt',encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            if "authors" in data:
                authors = data["authors"]  # authors list

                #match
                for author in authors:
                    result_file.write(str(count) + '\t' + str(author_dic.get(author)) + '\n' )
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1


def paper_conference(fileName):
    """Find the relationship between paper and the conference.Use mark number in conference.txt file.
    Input is the orginial data file contains this relation."""
    conference_dic = {}
    with open("conference.txt", encoding='utf-8') as conference_file:
        for line in conference_file:
            list = line.strip().split('\t') # number,abbreviation, full conference name
            conference_dic[list[2]] = list[0] #conference: mark number
    print(conference_dic)

    with open(fileName,encoding='utf-8') as data_file:
        count = 1
        result_file = open("paper-conference.txt",'wt',encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            if "publish" in data:
                conference = data["publish"]

                #match
                result_file.write(str(count) + '\t' + str(conference_dic.get(conference)) + '\n')
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1
    data_file.close()


def paper_proceeding(fileName):
    """Find relationship between paper and proceeding information
    Input is the orginial data file contains this relation."""
    proceeding_list = get_proceeding(fileName)
    print(proceeding_list)
    proceeding_dic = {}
    number = 1
    for proceeding in proceeding_list:
        proceeding_dic[proceeding] = int(number)
        number = number + 1
    print(proceeding_dic)

    with open(fileName,encoding='utf-8') as data_file:
        count = 1
        pattern = re.compile(r'.*\'\d+')  # match proceeding information
        result_file = open("paper-proceeding.txt",'wt',encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            if "proceeding" in data:
                proceeding = data["proceeding"].replace('\n', ' ')
                m = pattern.match(proceeding)
                if m is not None:  # matched
                    content = m.group().replace('Proceedings', '')
                    content = m.group().replace('Companion', '')
                    # match proceeding dictionary
                    result_file.write(str(count) + '\t' + str(proceeding_dic.get(content)) + '\n')
                else:# do not have specific proceeding informatino
                    print(count,"Unspeciafic proceeding information: ", proceeding)
                    result_file.write(str(count) + '\t' + '0' + '\n')

            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1
    data_file.close()


def paper_terms():
    """Use term.txt file and paper.txt file to find relationship between paper title and terms
    Use paper.txt file and term.txt file to get two attribute list"""
    term_dic = {}
    with open("term.txt",encoding='utf-8') as data_file:
        for line in data_file:
            content = line.strip().split('\t')
            term_dic[content[1]] = content[0]

    print(term_dic)

    result_file = open("paper-term.txt",'wt',encoding='utf-8')
    with open("paper.txt",encoding= 'utf-8') as data_file:
        count = 1
        for line in data_file:
            content = line.strip().split('\t') # 0-paper number , 1-title
            title = content[1]
            words = set(process_string(title))

            for word in words:
                if word in term_dic:
                    result_file.write(str(count) + '\t' + str(term_dic.get(word)) + '\n')

            count = count + 1
    data_file.close()


def author_institute(fileName):
    """Build relationship between author and institute. Input is the orginial data file contains this relation.
    Use author.txt to get authors list, use get_institutes(fileName) function in get_attribute.py to get institutes list """
    author_list = []
    with open("author.txt", encoding='utf-8') as author_file:
        for line in author_file:
            content = line.strip().split('\t')
            author_list.append(content[1])
    print(len(author_list))

    institute_list = get_institutes(fileName)
    print(len(institute_list))

    authors_institutes_dic = {}
    with open(fileName,encoding='utf-8') as data_file:
        for line in data_file:
            data = json.loads(line)

            if "authors"  not in data or "institutes" not in data:
                continue

            authors = data["authors"] # list
            institutes = data["institutes"] # list

            num = 0
            for author in authors:
                if author not in authors_institutes_dic: # add into dic
                    # institutes maybe less than authors number
                    if num <  len(institutes):
                        institute = institutes[num] # the author's institute
                    else:
                        institute = institutes[len(institutes)-1]
                    authors_institutes_dic[author] = institute
                num = num + 1
    print(authors_institutes_dic)
    data_file.close()
    sorted_dic = OrderedDict( sorted(authors_institutes_dic.items())) # sorted dict by authors
    print(sorted_dic)

    result_file = open("author-institute.txt",'wt',encoding='utf-8')
    for item in sorted_dic:
        author = author_list.index(item) + 1
        institute = institute_list.index(sorted_dic[item])+1
        print(item,author, sorted_dic[item],institute)
        result_file.write(str(author) + '\t' + str(institute) + '\n')
    result_file.close()


def reference(fileName):
    """Find papers' reference papers, build the relationship.
    Input is the orginial data file contains this relation."""
    paper_list = []
    with open("paper.txt",encoding='utf-8') as paper_file:
        for line in paper_file:
            content = line.split('\t')
            paper_list.append(content[1].strip() )
    paper_file.close()
    print(paper_list)

    result_file = open("reference.txt",'wt',encoding='utf-8')

    with open(fileName,encoding='utf-8') as data_file:
        count = 1 # paper counter
        for line in data_file:
            data = json.loads(line)
            if "refs" in data:
                refs = data["refs"]

                name_pattern = re.compile(r', [\w| |:|?|“|”|/|(|)|-]+, Proceeding')
                matched = 0 # flag: whether this sample has matched reference in paper list
                for reference in refs:
                    match = name_pattern.search(reference)
                    if match is not None:# matched
                        items = match.group().split(', ')
                        paper_name = items[1].strip()
                        if paper_name in paper_list: # has this paper in data file
                            matched = 1  # set flag
                            print(count, paper_name)
                            result_file.write(str(count) + '\t' + str(paper_list.index(paper_name)+1) + '\n')
                if matched == 0:
                    result_file.write(str(count) + '\t' + '0' + '\n')
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1
    data_file.close()


def cited_by(fileName):
    """Find the relation that paper is cited by other papers, build the relationship.
        Input is the orginial data file contains this relation."""
    paper_list = []
    with open("paper.txt", encoding='utf-8') as paper_file:
        for line in paper_file:
            content = line.split('\t')
            paper_list.append(content[1].strip())
    paper_file.close()
    print(paper_list)

    result_file = open("cited_by.txt",'wt',encoding='utf-8')
    with open(fileName,encoding='utf-8') as data_file:
        count = 1
        for line in data_file:
            data = json.loads(line)

            if "cite" in data:
                cite = data["cite"]
                name_pattern = re.compile(r', [\w| |:|?|“|”|/|(|)|-]+, Proceeding')
                matched = 0  # flag: whether this sample has 'cited-by paper' in paper list
                for item in cite:
                    match = name_pattern.search(item)
                    if match is not None:  # matched
                        items = match.group().split(', ')
                        paper_name = items[1].strip()
                        if paper_name in paper_list:  # has this paper in data file
                            matched = 1  # set flag
                            print(count, paper_name)
                            result_file.write(str(count) + '\t' + str(paper_list.index(paper_name)+1) + '\n')
                if matched == 0:
                    result_file.write(str(count) + '\t' + '0' + '\n')
            else:
                result_file.write(str(count) + '\t' + '0' + '\n')
            count = count + 1

        data_file.close()
