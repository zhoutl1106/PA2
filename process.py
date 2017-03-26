import ast

aggregateDic = {}
file = open('./out1.txt','rt')

def grabAWord(word):
    file.seek(0)
    ret = []
    while True:
        line = file.readline().strip();
        if line == "***":
            return ret;
        else:
            tempList = ast.literal_eval(line)
            if word == tempList[0]:
                return tempList[1]

def grabConsecutiveWords(words):
    words.pop(0)
    print("consecutive " , words)
    listOfPoss = []
    for word in words:
        l = grabAWord(word)
        if len(l) == 0:
            return []
        listOfPoss.append(grabAWord(word))
    ret = []
    for e in listOfPoss[0]:
        filename, start, line, offset = e.split('_')
        offset = int(offset)
        isConsecutive = True
        for i in range(1, len(listOfPoss)):
            tempP = filename + "_"+start + "_"+line + "_" + str(offset + i)
            if tempP not in listOfPoss[i]:
                isConsecutive = False
                break
        if isConsecutive:
            ret.append(e)
    return ret

def process(word):
    filestop = open('./stops.txt','rt')
    stopList = filestop.readline().strip().split()
    line = ""
    ret = ""

    # check if querying stop word
    allquery = word.split('+')
    pairedAllQuery=[]
    i = 0
    tempBuildQueryList = []
    while i < len(allquery):
        if i == 0:
            temp = ["and"]
        if (allquery[i] != "and") and (allquery[i] != "not") and (allquery[i] != "or"):
            temp.append(allquery[i])
        else:
            pairedAllQuery.append(temp)
            temp = [allquery[i]]
        i = i + 1
    pairedAllQuery.append(temp)

    for pair in pairedAllQuery:
        for i in range(1, len(pair)):
            if pair[i] in stopList:
                ret = "Your query contains a stop word : " + pair[i]
                return ret

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

    # query each word
    for pair in pairedAllQuery:
        ret = ret + "<h1>"+pair[0].upper() + "&nbsp,&nbsp"
        for i in range(1, len(pair)):
            ret = ret + pair[i] + " "
        ret = ret +"</h1> "
        if len(pair) == 2:
            listLoc = grabAWord(pair[1])
            if len(listLoc) == 0:
                ret = ret + "not exist"
            else:
                ret = ret + '<table style="width:100%"<tr><th>Filename</th><th>Line Num</th><th>Inline offset</th></tr>'
                for pos in listLoc:
                    filename, start, line, offset = pos.split('_')
                    realLine = int(line) + int(aggregateDic[start])
                    ret = ret + '<tr><th>' + filename + "</th><th>" +str(realLine) + "</th><th>" + offset+"</th></tr>"
                ret = ret + '</table>'
        else:
            listLoc = grabConsecutiveWords(pair)
            if len(listLoc) == 0:
                ret = ret + "not exist"
            else:
                ret = ret + '<table style="width:100%"<tr><th>Filename</th><th>Line Num</th><th>Inline offset</th></tr>'
                for pos in listLoc:
                    filename, start, line, offset = pos.split('_')
                    realLine = int(line) + int(aggregateDic[start])
                    ret = ret + '<tr><th>' + filename + "</th><th>" +str(realLine) + "</th><th>" + offset+"</th></tr>"
                ret = ret + '</table>'
    return ret
