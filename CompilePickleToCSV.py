import os
import csv
import pickle

local_path = (os.path.dirname(os.path.realpath('__file__')))
picklesfolder_path = os.path.join(local_path,"ASL Pickles")
CSV_PATH = os.path.join(local_path,'ASL-Data.csv')

print(picklesfolder_path)
print('-'*8)

def WriteNewCSVLine(listline):
    with open(CSV_PATH, 'a', newline='\n') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(listline)



for index, filename in enumerate(os.listdir(picklesfolder_path)):
    PICKLE_PATH = os.path.join(picklesfolder_path,filename)
    print(PICKLE_PATH)
    with open((PICKLE_PATH), 'rb') as f:
        timeline = pickle.load(f)

    if index == 0:
        Headings = ['letter']
        for i in range(0,len(timeline[0])):# create headings for the amount of elements in a frame of data
            Headings.append("unit-"+str(i))
        WriteNewCSVLine(Headings)

    letter = filename[0]
    for frame in timeline:
        frame.insert(0, letter)
        WriteNewCSVLine(frame)
        


