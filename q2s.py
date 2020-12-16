import csv
import json
from tqdm import tqdm
from stanfordcorenlp import StanfordCoreNLP
import logging
import sys
sys.path.append('./question-to-statement')
from POSTree import POSTree


header = ["sentence1", "sentence2", "title", "label"]

def convert(file_in, file_out, nlp):
    # try:
    count = 0
    with open(file_in) as f_in, open(file_out, 'w') as f_w:
        f_csv = csv.writer(f_w)
        f_csv.writerow(header)
        for line in f_in:
            qa = json.loads(line.strip())
            question = qa['question']
            question += '?'
            parser = nlp.parse(question)
            tree = POSTree(parser)
            try:
                statement = tree.adjust_order().replace(' **blank** ', ' ')
                # print("question: {}\nstatement:{}\n".format(question, statement))
                import pdb; pdb.set_trace()
                qa['statement'] = statement
                # import pdb; pdb.set_trace()
                if qa['answer']:
                    lable = 1
                else:
                    lable = 0
                example = [statement, qa['passage'], qa['title'], lable]
                f_csv.writerow(example)
                # f_w.write(json.dumps(qa) + "\n")
            except:
                print('Unknown question structure: {}\n{}\n'.format(question, parser))
                count += 1
    print("Unknown question structure: {}".format(count))


if __name__ == "__main__":
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    stanford_path = sys.argv[3]
    nlp = StanfordCoreNLP(stanford_path, logging_level=logging.DEBUG)
    try:
        convert(file_in, file_out, nlp)
    finally:
        nlp.close()
