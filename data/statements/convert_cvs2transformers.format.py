import os
import csv
import sys
import json
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert(input_file, output_dir):
    sent1_file = os.path.join(output_dir, "statements.sent1.json")
    sent3_file = os.path.join(output_dir, "statements.sent3.json")
    sent5_file = os.path.join(output_dir, "statements.sent5.json")
    f_in = open(input_file)
    f_sent1 = open(sent1_file, "w", encoding="utf-8")
    f_sent3 = open(sent3_file, "w", encoding="utf-8")
    f_sent5 = open(sent5_file, "w", encoding="utf-8")

    f_csv = csv.reader(f_in)
    header = None
    count = 0
    positive = 0
    negative = 0
    for row in f_csv:
        if not header:
            header = row
            # import pdb; pdb.set_trace()
            index_statement = header.index("statement")
            index_sent1 = header.index("raw_1sent")
            index_sent3 = header.index("raw_3sent")
            index_sent5 = header.index("raw_5sent")
            if "label" in header:
                index_label = header.index("label")
            else:
                index_label = None
                index_answer = header.index("answer")
        else:
            count += 1
            statement = row[index_statement].strip()
            sent1 = row[index_sent1].strip()
            sent3 = row[index_sent3].strip()
            sent5 = row[index_sent5].strip()
            if index_label:
                label = int(row[index_label])
            else:
                if row[index_answer] == "T":
                    label = 1
                else:
                    label = 0
            if label:
                positive += 1
            else:
                negative += 1
            f_sent1.write(json.dumps({"sentence1": statement, "sentence2": sent1, "label": label}) + "\n")
            f_sent3.write(json.dumps({"sentence1": statement, "sentence2": sent3, "label": label}) + "\n")
            f_sent5.write(json.dumps({"sentence1": statement, "sentence2": sent5, "label": label}) + "\n")
    logging.info("Total: {}; Positive: {}, Negative: {}".format(count, positive, negative))
    f_in.close()
    f_sent1.close()
    f_sent3.close()
    f_sent5.close()

if __name__  == "__main__":
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    convert(input_file, output_dir)
