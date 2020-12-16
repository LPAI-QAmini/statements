# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 22:54:32 2018

@author: Jacob
"""
import json
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag


def statement2question(statement):
    statement = statement.lower()
    statement = statement.replace('.','')
    question_keywords = ['is', 'will', 'are', 'was', 'were', 'am']

    word_decomp = statement.split(' ')

    for i in range(len(word_decomp)):
        if word_decomp[i] in question_keywords:
            for x in question_keywords:
                if word_decomp.count(x) >> 1:
                    
                    if pos_tag(word_decomp)[i+1][1] == 'VBN':
                        word_decomp.insert(0, word_decomp[i])
                        word_decomp.pop(i+1)
                    break
                else:
                    word_decomp.insert(0, word_decomp[i])
                    word_decomp.pop(i+1)
                    break
        else:
            if i == len(word_decomp) - 2:
                if word_decomp == statement.split(' '): # If statement unchanged
                    # Verb reduction:
                    for i in range(len(word_decomp)):
                        if 'VB' in pos_tag(word_decomp)[i][1]:
                            #print "BINGO"
                            word_decomp[i] = WordNetLemmatizer().lemmatize(word_decomp[i],'v')
                            #print "Verb reduction to present tense is required:"
                    word_decomp.insert(0, 'Did')
        
    for i in range(len(word_decomp)): # Cycle through all words
        #print str(np.array(pos_tag([word_decomp[i]]))[0][1])
        #print [word_decomp[i]]
        if 'NP' in str(np.array(pos_tag([word_decomp[i]]))[0][1]): # Searches for a proper noun
            word_decomp[i] = word_decomp[i].capitalize() # Capitalizes the proper noun
                    
    dot_to_que = word_decomp[len(word_decomp)-1].replace('.', '') # Deletes . at end of statement if it is there
    word_decomp.insert(0,word_decomp[0].capitalize()) # Capitalizes first word of statement
    word_decomp.pop(1) # Removes the possibly lowercase first word since the capitalized version has been inserted already
    question = (' ').join(word_decomp) # Create a string to reform the question instead of word by word
    # if '?' not in question: # Ensures that ? is attached to end of the statement
    #     question = question + '?' 
    
    return question 


def s2q(input_file, output_file):
    with open(input_file) as f_in, open(output_file, "w") as f_w:
        count = 0
        for line in f_in:
            sample = json.loads(line.strip())
            statement = sample["sentence1"]
            try:
                question = statement2question(statement=statement)
            except:
                question = statement
            if sample["label"] == 1:
                count += 1
            sample["sentence1"] = question
            f_w.write(json.dumps(sample) + "\n")
        print(count)


if __name__ == "__main__":
    #statement = input("Enter an English sentence to be transformed into a question: \n")    #'There will be a book here.'
    #question = statement2question(statement=statement)
    #print(question)     #Return the final formed question version of the input statement
    
    # file_in = "./temp/yeqiu.json"
    # file_out = "./temp/yeqiu.s2q.json"
    # with open(file_in) as f_obj, open(file_out, "w") as f_w:
    #     data = json.load(f_obj)
    #     for idx, items in data.items():
    #         for item in items:
    #             statement = item["raw"]
    #             try:
    #                 question = statement2question(statement=statement)
    #                 case = {"statement": statement,
    #                         "question": question}
    #             except:
    #                 # print("Conversation Failed.")
    #                 case = {"statement": statement,
    #                         "question": "Non"}
    #             f_w.write(json.dumps(case) + "\n")
    input_file = "./data/statements_v0.0.json"
    output_file = "./data/statements_v0.0.question.json"
    s2q(input_file, output_file)
