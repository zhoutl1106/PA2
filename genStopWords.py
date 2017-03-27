file = open('./out0.txt','rt')

total = 0   # total number of appearance of all words
wordCnt = 0 # different words
for line in file:
    line = line.strip()
    word,cnt = line.split()
    total = total + int(cnt)
    wordCnt = wordCnt + 1

# pick 5 time average frequency as threshold
threshold = total / wordCnt * 5
print(threshold)
file.seek(0)

file1 = open('./stops.txt','wt')
for line in file:
    line = line.strip()
    word,cnt = line.split()
    cnt = int(cnt)
    # considered as stop word
    if cnt > threshold:
        file1.write(word+" ")
