

import csv
import random

input_file_name="../dataset1/labeled_data_numeric.csv"
output_file_name= "labeled_data_numeric.csv"
with open(input_file_name, 'r') as f:
    file_lines = [','.join([format(random.randint(1, 15)),x]) for x in f.readlines()]

with open(output_file_name, 'w') as f:
    f.writelines(file_lines)

f.close()