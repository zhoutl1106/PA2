import ast

aggregateDic = {}
file = open('./out1.txt','rt')

def grabAWord(word):
    file.seek(0)
    ret = []
    # read in each line to find querying word
    while True:
        line = file.readline().strip();
        if line == "***":
            return ret;
        else:
            tempList = ast.literal_eval(line)
            if word == tempList[0]:
                return tempList[1]

def grabConsecutiveWords(words1):
    # remove the leading logical and/or/not
    words = words1[:]
    words.pop(0)
    # print("conse ", words)
    listOfPoss = []
    # query each word in word group
    for word in words:
        l = grabAWord(word)
        if len(l) == 0:
            return []
        listOfPoss.append(grabAWord(word))
    ret = []

    # assume the first element must be contained
    for e in listOfPoss[0]:
        filename, start, line, offset = e.split('_')
        offset = int(offset)
        isConsecutive = True
        # check all the other words are consecutive
        for i in range(1, len(listOfPoss)):
            tempP = filename + "_"+start + "_"+line + "_" + str(offset + i)
            if tempP not in listOfPoss[i]:
                isConsecutive = False
                break
        # if survived for all check, add it to return value
        if isConsecutive:
            ret.append(e)
    return ret

def andList(a_list, b_list):
    ret_list = []
    for e in a_list:
        filename, start, line, offset = e.split('_')
        for g in b_list:
            filename1, start1, line1, offset1 = g.split('_')
            if filename1 == filename and start1 == start and line1 == line and offset1 != offset:
                ret_list.append(e)

    # print ("andList : ", a_list, b_list, ret_list)
    return ret_list

def orList(a,b):
    ret_list = list(set(a).union(set(b)))
    # print ("orList : ", a, b, ret_list)
    return ret_list

def notList(a_list, b_list):
    ret_list = a_list[:]
    for e in a_list:
        filename, start, line, offset = e.split('_')
        for g in b_list:
            filename1, start1, line1, offset1 = g.split('_')
            if filename1 == filename and start1 == start and line1 == line:
                ret_list.remove(e)
    # print ("notList : ", a_list, b_list, ret_list)
    return ret_list


def process(word):
    filestop = open('./stops.txt','rt')
    stopList = filestop.readline().strip().split()
    line = ""
    ret = ""
    word = word.lower();

    # check if querying stop word
    allquery = word.split('+')
    pairedAllQuery=[]
    i = 0
    tempBuildQueryList = []
    while i < len(allquery):
        if i == 0:
            temp = ["or"]
        if (allquery[i].lower() != "and") and (allquery[i].lower() != "not") and (allquery[i].lower() != "or"):
            temp.append(allquery[i].lower())
        else:
            pairedAllQuery.append(temp)
            temp = [allquery[i]]
        i = i + 1
    pairedAllQuery.append(temp)
    # print("all query ", pairedAllQuery)

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
    queryResult = []
    for pair in pairedAllQuery:
        tempWord = ""
        for i in range(1, len(pair)):
            tempWord = tempWord + pair[i] + " "
        if len(pair) == 2:
            listLoc = grabAWord(pair[1])
        else:
            listLoc = grabConsecutiveWords(pair)
        queryResult.append([tempWord, pair[0], listLoc])

    # process logical

    logicalRet = []


    for i in queryResult:
        ret = ret + "<h1>Single Query Result : " + i[0] + "</h1>"
        if len(i[2]) == 0:
            ret = ret + "not exist"
        else:
            ret = ret + '<table style="width:100%"<tr><th>Filename</th><th>Line Num</th><th>Inline offset</th></tr>'
            for pos in i[2]:
                filename, start, line, offset = pos.split('_')
                realLine = int(line) + int(aggregateDic[start])
                ret = ret + '<tr><th>' + filename + "</th><th>" +str(realLine) + "</th><th>" + offset+"</th></tr>"
            ret = ret + '</table>'

    for i in queryResult:
        if len(i[2]) == 0:
            ret = ret + " logical not exist"
            return ret
        else:
            if i[1].upper() == "AND":
                logicalRet = andList(logicalRet, i[2])
            elif i[1].upper() == "OR":
                logicalRet = orList(logicalRet, i[2])
            elif i[1].upper() == "NOT":
                logicalRet = notList(logicalRet, i[2])

    ret = ret + "<h1>Logical Result : " + word.replace('+',' ') + "</h1>"
    ret = ret + '<table style="width:100%"<tr><th>Filename</th><th>Line Num</th><th>Inline offset</th></tr>'
    for pos in logicalRet:
        filename, start, line, offset = pos.split('_')
        realLine = int(line) + int(aggregateDic[start])
        ret = ret + '<tr><th>' + filename + "</th><th>" +str(realLine) + "</th><th>" + offset+"</th></tr>"
    ret = ret + '</table>'
    return ret
