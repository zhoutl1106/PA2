from process import grabAWord
import sys
import ast

word = sys.argv[1]
aggregateDic = {}

file = open('./out1.txt','rt')
filestop = open('./stops.txt','rt')
stopList = filestop.readline().strip().split()
line = ""
ret = ""
allquery = word.split('+')
if(word in stopList):
    print("Your query contains a stop word : " + word)
    quit()

# build chunk lines dictionary
while True:
    line = file.readline();
    if line.strip() == "***":
        break;
line = file.readline();
dic = ast.literal_eval(line)
temp = 0;
lastValue = 0
first = True
for key,value in dic.iteritems():
    if first:
        aggregateDic[key] = "0"
        temp = value
        first = False
        continue
    aggregateDic[key] = temp
    temp = temp + value

# check that word
listPos = grabAWord(word)

print("You're querying : "+word)
if len(listPos) == 0 :
    print("  Not exist")
    quit()
for pos in listPos:
    filename, start, line, offset = pos.split('_')
    realLine = int(line) + int(aggregateDic[start])
    print("  file: "+filename + "\tline: " + str(realLine) + "\t inline offset: " + offset)
