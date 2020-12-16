from question_to_statement.POSTree import POSTree
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'/home/rthuang/script/stanford-corenlp-full-2018-10-05')

sentence = 'Is the boy holding a toy?'

try:
    parser = nlp.parse(sentence)
    print(parser)
    tree = POSTree(parser)
    print(tree.adjust_order().replace('**blank**', ''))
    # print(nlp.dependency_parse(sentence))
finally:
    nlp.close()