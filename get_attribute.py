# -*- coding: utf-8 -*-
import json
import nltk
import re

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


"""
from pprint import pprint
with open('key2_result', encoding = 'utf-8') as data_file:
    line = data_file.readline()
    data = json.loads(line)
    pprint(data)
    print(data["abstract"])
    for item in data["authors"]:
        print(item, end=',')
    #print(data["authors"])
    print('\t')
    for item in data["cite"]:
        print(item,end=' ')
    #print(data["cite"])
    print('\t')
    print(data["index_term"])
    for item in data["institutes"]:
        print(item, end=',')
    #print(data["institutes"])
    print('\t')
    print(data["publish"])
    for item in data["refs"]:
        print(item, end='')
    #print(data["refs"])
    print('\t')
    print(data["title"])
"""


def get_paper(fileName):
    """Input is the file name.
    This function is used for getting [paper.txt] file.
    Directly get title from original json file.
    Note: split by Tab"""
    with open(fileName, encoding='utf-8') as data_file:
        count = 1
        file = open('paper.txt','wt',encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            print(count,data["title"])
            file.write(str(count) +'\t'+ data["title"] +'\n')

            count = count +1

    data_file.close()


def get_term(limit):
    """Read paper.txt file for title and extract terms from title, write terms of title into terms.txt file.
    Input limit used for set the least frequency of chosen words"""
    title_list = []
    with open("paper.txt", encoding='utf-8') as data_file:
        for line in data_file:
            item = line.strip().split('\t')
            title = item.pop().strip().lower()
            title_list.append(title)

    title_text = ' '.join(title_list)
    title_list = process_string(title_text) # title terms list after processing
    fdist = nltk.FreqDist( nltk.Text(title_list))

    output = open('term.txt', 'wt', encoding='utf-8')
    count = 1
    for tuple in fdist.most_common():
        print(tuple[0], " ", tuple[1])

        if tuple[1] < limit: # low-frequency words
            continue

        output.write(str(count) + '\t' + tuple[0] + '\t'+ str(tuple[1])+ '\n')
        count = count + 1


def get_feature(fileName):
    """This function is used for generate a feture matrix of all samples.
    Output feature.txt, of which each line is a sample and each column is a word feature.
    It calls feature_word_frequency() for getting feature words list"""

    #get_abstract(fileName)
    feature = feature_word_frequency(20) # a word feature list sorted by frequency, word frequency > 20
    result_file = open('feature.txt', 'wt', encoding='utf-8')
    with open(fileName, encoding='utf-8') as data_file:
        count = 1;
        for line in data_file:
            data = json.loads(line)
            print("SAMPLE ", count)
            count = count+1
            title = data["title"].strip('\n').lower()
            if "abstract" in data:
                abstract = data["abstract"].replace('\n',' ').lower()
            else:
                abstract = "An abstract is not available."

            text = title +' '+ abstract
            words_list = process_string(text)

            # match sample words to feature word as well as count
            for f in feature:
                if f in words_list:
                    result_file.write( str(words_list.count(f)) + '\t')
                else:
                    result_file.write("0" + '\t')

            result_file.write('\n') # end write a sample
    data_file.close()


def get_abstract(fileName):
    """This function is used for getting abstract from original file and write into abstract.txt"""
    with open(fileName, encoding='utf-8') as data_file:
        count = 1
        file = open('abstract.txt','wt',encoding='utf-8')
        for line in data_file:
            data = json.loads(line)
            # if abstract is not exist, write "An abstract is not available."
            try:
                # Note: some abstract contains '\n' and '\t' which should be removed
                abstract = data["abstract"].replace('\n',' ')
                abstract = abstract.replace('\t',' ')
                print(count,abstract)
                file.write(str(count) +'\t'+ abstract +'\n')
            except:
                print(count,"No abstract!!!")
                file.write(str(count) + '\t' + "An abstract is not available." +'\n')

            count = count +1
    data_file.close()


def feature_word_frequency(frequency):
    """Input is the feature words frequency, when a word's frequency larger than this value, it's chosen as feature.
    This function is used for extracting feature from abstract and title of all samples.
    In the result file, each line represents a sample's abstract, and each column is a feature word.
    The value is word frequency
    Return feature list, sorted by frequency"""

    print("FUNCTION: feature_word_frequency: ", frequency)
    text = []
    # abstract
    with open("abstract.txt", encoding = 'utf-8') as data_file:
        for line in data_file:
           item = line.strip().split('\t')
           text.append(item.pop(1).strip('\n').lower()) # all in lowcase

    # title
    with open("paper.txt",encoding='utf-8') as title_file:
        for line in title_file:
            item = line.strip().split('\t')
            text.append(item.pop().strip().lower())

    text_string = ' '.join(text)
    #process text string
    words_list = process_string(text_string)

    #calculate frequence
    fdist = nltk.FreqDist( nltk.Text(words_list) )
    #print(fdist.most_common() )

    #write all feature words into a file
    output = open('abstract_title_feature','wt',encoding='utf-8')
    count = 1
    feature = []
    for tuple in fdist.most_common():
        # only use high-frequency words as the feature
        if tuple[1] >= frequency:
            feature.append(tuple[0])
            print(tuple[0], " ", tuple[1])

        output.write(str(count) + '\t' + tuple[0] +'\t'+ str(tuple[1]) +'\n')
        count = count + 1

    return feature


def process_string(string):
    """This functio is used for processing string, including tokenizing, removing stop words and lemmatizing.
    Input a string needing to be process,
    Return a word list of this string( Note: Contains repeating words!!!)"""
    # tokenize
    print("Start tokenizing...")
    # split text into tokens and remove punctuation and numeric character
    tokens = nltk.RegexpTokenizer(r'[a-z]+').tokenize(string)
    print("Tokens length: ",len(tokens))

    # delete stop words
    print("Start deleting stop words...")
    stopwords_list = build_stopwords_list()
    vocabulary = []
    for word in tokens:
        if word not in stopwords_list:
            vocabulary.append(word)
    print("Vocabulary length: ",len(vocabulary))
    # print(vocabulary)

    # words tagging
    print("Start words tagging...")
    vocabulary_tag = nltk.pos_tag(vocabulary)
    # print(vocabulary_tag)

    # lemmatization
    print("Start limmatizing...")
    lemmatizer = WordNetLemmatizer()
    words_list = []
    for tuple in vocabulary_tag:
        word = lemmatizer.lemmatize(tuple[0], pos=get_wordnet_pos(tuple[1]))  # get normal words
        # print(word)
        if word not in stopwords_list:
            words_list.append(word)
    print("The number of words: ",len(set(words_list)))
    return words_list


def get_wordnet_pos(treebank_tag):
    """This function is used for transform tree bank pos tag into wordnet compatible pos tag"""

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:# default value NOUN
        return wordnet.NOUN


def build_stopwords_list():
    """This function read StopWords_EN.txt file, the stop words are from [http://www.ranks.nl/stopwords]
    Return a stopwords list"""
    stop_words = []
    with open("StopWords_EN.txt", encoding = 'utf-8') as words_file:
        for word in words_file:
            stop_words.append(word.strip('\n') )
    #print(stop_words)
    return stop_words


def get_index_term(fileName):
    """This function is used for getting index_term.txt file which contains each samples index_term information
    Input the priginal file name"""
    with open(fileName, encoding= 'utf-8') as data_file:
        # calculate index_term
        index_list = []

        num = 1
        for line in data_file:
            data = json.loads(line)

            if "index_term" in data:
                index_term = data["index_term"].strip()
                print(num,index_term)
                num = num + 1
                if index_term not in index_list:
                    index_list.append(index_term)

        print(index_list)
        print(num)
        output = open('index_term.txt', 'wt', encoding='utf-8')
        count = 1
        for i in index_list:
            output.write(str(count) + '\t' + i +'\n')
            count = count + 1


def get_author(fileName):
    authors_list = []
    with open(fileName,encoding='utf-8') as data_file:
        for line in data_file:
            data = json.loads(line)
            if "authors" not in data:
                continue
            print(data["authors"])
            authors_list = authors_list + data["authors"]

    authors = sorted(set(authors_list))

    output = open("author.txt", 'wt', encoding='utf-8')
    count = 1
    for author in authors:
        print(count, author)
        output.write(str(count) + '\t' + author + '\n')
        count = count +1

    output.close()


def get_institutes(fileName):
    """Extract insititutes information from original data, Output insititutes.txt """
    institutes_list=[]
    with open(fileName,encoding='utf-8') as data_file:
        for line in data_file:
            data = json.loads(line)
            if "institutes" in data:
                #print(data["institutes"])
                institutes_list = institutes_list + data["institutes"]

    institutes_list = sorted(set(institutes_list))
    output = open("insititutes.txt", 'wt', encoding='utf-8')
    count = 1
    for institute in institutes_list:
        print(count, institute)
        content = institute.split(',')
        output.write(str(count) )
        for item in content:
            output.write('\t'+ item.replace('"','' ))
        output.write('\n')

        count = count + 1

    output.close()


def get_proceeding(fileName):
    """Get proceeding information from original data, Some proceeding information is missing.
    Output proceeding.txt file, including the conference abbreviation and the year"""
    with open(fileName, encoding='utf-8') as data_file:
        proceeding_list = []
        pattern = re.compile(r'.*Proceedings') # match proceeding information
        for line in data_file:
            data = json.loads(line)

            if "proceeding" in data:
                proceeding = data["proceeding"].replace('\n',' ')
                m = pattern.match(proceeding)
                if m is not None: # matched
                    content = m.group().replace('Proceedings',' ')
                    proceeding_list.append(content)



        proceeding_list = sorted(set(proceeding_list))
        #print(proceeding_list)
        count = 1
        output = open("proceeding.txt", 'wt', encoding='utf-8')
        p = re.compile(r'[0-9]+')
        for proceeding in proceeding_list:
            print(proceeding)
            proceeding = proceeding.replace('\'',' ' )
            pro_items = proceeding.split(' ')  # get conference information
            output.write(str(count) + '\t'+ pro_items[0] + '\t')
            count = count + 1

            a = p.search(proceeding).group()
            year = int( a) # get year
            if year < 20: # 2000s
                year = 2000+year
            else: # 1900s
                year = 1900+year
            output.write(str(year) + '\n')


def get_conference(fileName):
    """ Get all "conference inforamtion from original data.
    Output is conference.txt file contains all conference and their abbreviation."""
    conference_list = []
    count = 0
    with open(fileName,encoding='utf-8') as data_file:
        for line in data_file:
            data = json.loads(line)
            count = count + 1
            if "publish" in data:
                print(count,data["publish"],'          ',data["title"])
                conference_list.append(data["publish"].strip())

    conferences = sorted(set(conference_list))

    output = open("conference.txt", 'wt', encoding='utf-8')
    count = 1
    for conference in conferences:
        print(count, conference)
        # get all uppercase letters as the abbreviation
        abbreviation = ''.join([char for char in conference if char.isupper()] )
        output.write(str(count) + '\t' + abbreviation +'\t'+ conference + '\n')
        count = count + 1

    output.close()


