import csv
infileName = 'olddata.csv'
outfileName = 'item.csv'

items = dict()
with open(infileName, 'r', encoding = 'utf-8') as infile:
    input = csv.reader(infile)
    for line in input:
        if line[2] not in items:
            items[ line[2] ] = [ line[2], line[3], line[5] ]

with open(outfileName, 'w', encoding = 'utf-8') as outfile:
    output = csv.writer(outfile, delimiter = ',')
    for i in items:
        output.writerow(items[i])
