file = open('./out0.txt','rt')

total = 0
wordCnt = 0
for line in file:
    line = line.strip()
    word,cnt = line.split()
    total = total + int(cnt)
    wordCnt = wordCnt + 1

threshold = total / wordCnt * 5
print(threshold)
file.seek(0)

file1 = open('./stops.txt','wt')
for line in file:
    line = line.strip()
    word,cnt = line.split()
    cnt = int(cnt)
    if cnt > threshold:
        file1.write(word+" ")
