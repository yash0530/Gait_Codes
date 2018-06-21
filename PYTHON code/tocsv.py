file2 = open('data.csv', 'w')
data = 
for list in data:
    for reading in list:
        file2.write(str(reading) + ',')
    file2.write('\n')
file2.close()