import os
import argparse
import random

import pandas  




parser = argparse.ArgumentParser("prepara texto")
parser.add_argument("-i","--input",type=str, default='/mnt/datasets/Squad_2.0/SQuAD_csv.csv' )
parser.add_argument("-p","--percent_train",type=float, default=0.8)
parser.add_argument("-pd","--percent_discard",type=float, default=0.5)

args = parser.parse_args()
input_file = args.input
percent_train = args.percent_train
percent_discard= args.percent_discard


colnames = ['index', 'context', 'question','id','answer_start','text']
data = pandas.read_csv(input_file, names=colnames)

context=data.context.tolist()
questions=data.question.tolist()
answers=data.text.tolist()

ofilev = open('validation.csv', 'w')
ofilet = open('train.csv', 'w')
ofile_out = open('out_of_sample.csv', 'w')
ofile_discarted = open('discarted.csv', 'w')

countt = 0
countv = 0
count_out = 0
count_disc = 0

ofilev.write(",text\n")
ofilet.write(",text\n")
ofile_out.write(",text\n")
ofile_discarted.write(",text\n")

index = 1
max_len = 0

random.seed(42)

while(index<len(context)):

    tupla = '<|endoftext|>context: '+str(context[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip() + \
            '\nquestion: ' +        str(questions[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip() + \
            '\nanswer: ' +          str(answers[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip() + '<|endoftext|>'

    if len(tupla) <1024:

        if random.random() > percent_discard:    
            if random.random() > percent_train:
                ofilev.write("{},\"{}\"\n".format(countv,tupla))
                countv+=1
            else:

                ofilet.write("{},\"{}\"\n".format(countt,tupla))
                countt+=1
        else:

            ofile_out.write("{},\"{}\"\n".format(count_out,tupla))
            count_out+=1

        if len(tupla)>max_len:

            max_len = len(tupla)

    else:
        ofile_discarted.write("{},\"{}\"\n".format(count_disc,tupla))
        count_disc +=1
        #if max_len > 3000:
        #    print ('--------------------------------------------------\n')
        #    print(tupla)
        #    print ('--------------------------------------------------\n')

    index +=1


print("max len:", max_len)
print("train.csv samples: {}\n".format(countt))
print("validation.csv samples: {}\n".format(countv))
print("out_of_sample.csv samples: {}\n".format(count_out))
print("discarted.csv samples: {}\n".format(count_disc))

ofilev.close()
ofilet.close()
ofile_out.close()
ofile_discarted.close()


