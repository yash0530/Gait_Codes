import sys
readfile = sys.argv[1]
writefile = sys.argv[2]

read = open(readfile, 'r')
write = open(writefile, 'w')
rows = read.readlines()

write.write('[')
for i in range(len(rows)):
    row = rows[i].split('\t')
    if row[-1] == '':
        row = row[:-1]
    else:    
        row[-1] = row[-1].strip('\n')
    write.write(str(row))
    if i != len(rows) - 1:
       write.write(',\n') 
write.write(']')
