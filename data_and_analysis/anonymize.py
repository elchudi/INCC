import csv
import os

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('./') if isfile(join('./', f))]
onlycsv = [x for x in onlyfiles if (x[-4:] == ".csv"  or x[-4:] == ".log") and "data_digested" not in x and 'row_per_user' not in x]
print(len(onlycsv))

f_to_number = {}
for filename in onlycsv:
    filename_key = filename[:10]
    if filename_key in f_to_number.keys():
        number = f_to_number[filename_key]
    else:
        number = 1 + max([0] + [v for k,v in f_to_number.items()])
        f_to_number[filename_key] = number
    with open(filename, 'r') as inn:
        with open('./anon/' + str(number) + filename[filename.index("_"):], 'w') as out:
            out.write(inn.read())
