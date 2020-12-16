import sys
import json

def convert(file_in, file_out):
  with open(file_in) as f_in, open(file_out, "w") as f_w:
    for line in f_in:
      item = json.loads(line.strip())
      sentence1 = item["question"]
      sentence2 = item["passage"]
      if item["answer"]:
        label = 1
      else:
        label = 0
      sample = {
        "sentence1": sentence1,
        "sentence2": sentence2,
        "label": label
      }
      f_w.write(json.dumps(sample) + "\n")
      # import pdb; pdb.set_trace()


if __name__ == "__main__":
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  convert(input_file, output_file)