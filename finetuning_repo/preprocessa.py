import os
import argparse
import random

parser = argparse.ArgumentParser("prepara texto")
parser.add_argument("-i","--input",type=str )
parser.add_argument("-p","--percent_train",type=float)
args = parser.parse_args()
input_file = args.input
percent_train = args.percent_train

# Opening file
ifile = open(input_file, 'r')

ofilev = open('validation.csv', 'w')
ofilet = open('train.csv', 'w')

countt = 0
countv = 0

ofilev.write(",text\n")
ofilet.write(",text\n")

block = ""

for line in ifile:
    
    if len(block)<800:
        block = block + line
    else:
        #tupla = '<|endoftext|>' + block.replace("\n"," ").replace("“","'").replace("\"","'").replace("”","'") + '<|endoftext|>'
        tupla = '<|endoftext|>' + block.replace("“","'").replace("\"","'").replace("”","'") + '<|endoftext|>'
        if random.random() > percent_train:
            ofilev.write("{},\"{}\"\n".format(countv,tupla))
            countv+=1
        else:

            ofilet.write("{},\"{}\"\n".format(countt,tupla))
            countt+=1
        block = ""


print("train.csv samples: {}\n".format(countt))
print("validation.csv samples: {}\n".format(countv))
ifile.close()
ofilev.close()
ofilet.close()