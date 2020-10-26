def getListContents(file):
    fileName = 'auction/choicesText/'+file+'.txt'
    items = open(fileName, 'r').read()
    itemList = items.split('\n')
    finalList = []
    for listNum in range(len(itemList)):
        finalList.append((itemList[listNum],itemList[listNum]))
    return finalList
