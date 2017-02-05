import re
from collections import OrderedDict
from operator import itemgetter

#Input parameter-file values
dictionaryMIS = OrderedDict({})
dictionaryI=OrderedDict({})
sortedDictionaryMIS ={}
cannotBeTogether = []
mustHave = []
SDC = 0.0
listOfTrasactions = []
listOfItems = []
listL = []
listF1 = []
listFk = []
dictionaryFk = {}
dictionaryTail = OrderedDict({})

# MS-APRIORI ALGORITHM
def msApriori():
    listCk = []
    # CALL TO THE INIT_PASS FUNCTION
    init_pass()
    # CALL TO COMPUTE THE F1 FREQUENT ITEM SETS
    computeF1()
    k = 2
    dictionaryFk[1] = listF1
    while(len(dictionaryFk[k-1]) != 0):
#    while( k == 2):
        dictionaryCount = OrderedDict({})
        dictionaryTailCount = OrderedDict({})
        if k == 2:
            listCk = computeC2()
        else:
            listCk = msCandidateGen(dictionaryFk[k-1])
        # BREAK THE LOOP IF CK IS EMPTY
        if not listCk:
            break
#        print("C",k, ": ", listCk)
        for transaction in listOfTrasactions:
            for candidate in listCk:
                lengthOfCandidate = len(candidate)
                lengthOfTailCandidate = len(candidate) - 1
                for eachCandidate in candidate:
                    if eachCandidate in transaction:
                        lengthOfCandidate = lengthOfCandidate - 1
                candidateString = ','.join(candidate)

                for eachCandidate in candidate[1:]:
                    if eachCandidate in transaction:
                        lengthOfTailCandidate = lengthOfTailCandidate -1
                tailCandidateString = ','.join(candidate[1:])

                if(lengthOfCandidate == 0):
                    if(candidateString in dictionaryCount.keys()):
                        dictionaryCount[candidateString] = dictionaryCount[candidateString] + 1
                    else:
                        dictionaryCount[candidateString] = 1
                elif(candidateString not in dictionaryCount.keys()):
                    dictionaryCount[candidateString] = 0
# TAILCOUNT
                if(lengthOfTailCandidate == 0):
                    if tailCandidateString not in dictionaryTail.keys():
                        calTailCount(tailCandidateString)
        listOfC = []
        for c in listCk:
            stringC = ','.join(c)
            if(dictionaryCount[stringC]/len(listOfTrasactions) >= dictionaryMIS[ c[0] ]):
                if c not in listOfC:
                    listOfC.append(c)
        dictionaryFk[k] = listOfC

        printFunction(k, dictionaryTail, dictionaryFk[k])
#        print("\ndictionary tail count: ", dictionaryTailCount)
#        print("\nF", k, ": ", dictionaryFk[k])
#        print("END OF ONE ITERATION\n")
        k = k + 1

def calTailCount(tailString):
    for transaction in listOfTrasactions:
        flag = True
        for item in str.split(tailString,','):
            if item not in transaction:
                flag = False
                break
        if flag == True:
            if tailString in dictionaryTail.keys():
                dictionaryTail[tailString] = dictionaryTail[tailString] + 1
            else:
                dictionaryTail[tailString] = 1
    if tailString not in dictionaryTail.keys():
        dictionaryTail[tailString] = 0


def msCandidateGen(listFkMinus1):
    #EMPTY THE CANDIDATE LIST Ck
    listCk = []

    for i in range(0,len(listFkMinus1)):
        for j in range (i+1,len(listFkMinus1)):

            similarityFlag = True

            for l in range(0,len(listFkMinus1[i])):
               if(listFkMinus1[i][l] != listFkMinus1[j][l]):
                    similarityFlag = False
                    break
            if similarityFlag == True:
                continue
            flag = 1
            for k in range( 0,len(listFkMinus1[i]) - 1 ):
                if(listFkMinus1[i][k] != listFkMinus1[j][k]):
                    flag = 0
                    break
            if(flag == 1):
#                if( dictionaryMIS[listFkMinus1[i][len(listFkMinus1[i]) - 1]] <= dictionaryMIS[listFkMinus1[j][len(listFkMinus1[i]) - 1]]) \
#                        and (abs(dictionaryI[listFkMinus1[i][len(listFkMinus1[i]) - 1]] - dictionaryI[(listFkMinus1[j][len(listFkMinus1[i]) - 1])]) <= SDC):
                 if(abs(dictionaryI[listFkMinus1[i][len(listFkMinus1[i]) - 1]] - dictionaryI[(listFkMinus1[j][len(listFkMinus1[i]) - 1])]) <= SDC):
                    listC = []
                    listC = listFkMinus1[i][:]
                    listC.append(listFkMinus1[j][len(listFkMinus1[i]) - 1])

                    count = 0
                    for eachItem in listC:
                        if eachItem in cannotBeTogether:
                            count = count + 1
                    if count < 2:
                        listCk.append(listC)
                    else:
                        continue
                    subSetList = []

                    for m in range(0, len(listC)):
                        if (m == 0):
                            for n in range(m + 1, len(listC)):
                                listSub = []
                                listSub.append(listC[m])
                                if (len(listC[m + 1:n]) != 0):
                                    listSub = listSub + listC[m + 1:n]
                                if (len(listC[n + 1:]) != 0):
                                    listSub = listSub + listC[n + 1:]
                                subSetList.append(listSub)
                        else:
                            subSetList.append(listC[m:])
                            break;
                    for subSet in subSetList:
                        if (listC[0] in subSet) or ( dictionaryMIS[listC[1]] == dictionaryMIS[listC[0]] ):
                            if subSet not in listFkMinus1:
                                listCk.remove(listC)
    return listCk
def modifyListForMustHave(k,listFk):
    listResult = []
    for item in listFk:
        if k==1:
            if item in mustHave:
                listResult.append(item)
        else:
            flag = False
            for val in item:
                if val in mustHave:
                    flag = True
                    break
            if flag == True:
                listResult.append(item)
    return listResult
def printFunction(k, dictionaryTailCount , listFk):
    finalList = modifyListForMustHave(k,listFk)
    if len(finalList)!=0:
        dictionaryFrequency = {}
        count = 0
        if(k == 1):
            print("Frequent 1-itemsets\n")

            for item in finalList:
                print("\t"+str(listOfItems.count(item))+ ' : {'+ str(item)+ '}')
        else:
            print("Frequent ", k,"-itemsets\n")

            for item in finalList:
                    itemSubString = ','.join(item[1:])
                    itemString =','.join(item)
                    printString = ', '.join(item)
                    dictionaryFrequency = computeFrequency(listFk)
                    print("\t"+str(dictionaryFrequency[itemString])+" : {"+ printString+ "}")
                    print("Tailcount = ",dictionaryTailCount[itemSubString])
        print("\n\tTotal number of frequent "+ str(k) + "-itemsets = "+str(len(finalList)),"\n\n")

#USED FOR COMPUTING FREQUENCY OF EACH ITEMSET IN THE SET OF TRANSACTIONS
def computeFrequency(listFk):

    dictionaryFrequency = {}
    for eachSubSet in listFk:
        tempCount = 0
        for transaction in listOfTrasactions:
            flag = 1
            for item in eachSubSet:
                if item not in transaction:
                    flag = 0
                    break
            if flag == 1:
                tempCount = tempCount + 1
        eachSubSetString = ','.join(eachSubSet)
        dictionaryFrequency[eachSubSetString] = tempCount
    return dictionaryFrequency

def init_pass():
    # SCAN THE DATA AND RECORD THE SUPPORT
    setOfItems = []
    numberOfTransactions = myTransactions.__len__();
    for transaction in listOfTrasactions:
        for item in transaction:
            listOfItems.append(item)
            if item not in setOfItems:
                setOfItems.append(item)

    #setOfItems = set(listOfItems)
    for item in setOfItems:
        supportCountOfItem = listOfItems.count(item)
        support = round((supportCountOfItem/numberOfTransactions),4)
        dictionaryI[item] = support
    # DELETE ITEMS IN dictionaryMIS IF THEY ARE NOT PRESENT IN SETOFITEMS
    for key,value in dictionaryMIS.items():
        if key not in setOfItems:
            del dictionaryMIS[key]

    # STEPS FOR FORMING L
    for key,value in dictionaryMIS.items():
        if(dictionaryI[key] >= dictionaryMIS[key]):
            listL.append(key)
            break
    for key,value in dictionaryMIS.items():
        if( dictionaryMIS[listL[0]] <= dictionaryMIS[key] and (dictionaryI[key] >= dictionaryMIS[listL[0]]) and key != listL[0] ):
            listL.append(key)

# FUNCTION TO COMPUTE THE LEVEL 2 CANDIDATE GENERATION
def computeC2():
    listC2 =[]
    for itemL in range(0,len(listL)):
        if(dictionaryI[ listL[itemL] ] >= dictionaryMIS[ listL[itemL]] ):
            for itemH in range(itemL+1, len(listL)):
                if(dictionaryI[ listL[itemH] ] >= dictionaryMIS[ listL[itemL] ] ) and ( abs(dictionaryI[listL[itemH]]-dictionaryI[listL[itemL]]) <= SDC ):
                    twoItemsList = []
                    count = 0
                    if listL[itemL] in cannotBeTogether:
                        count = count + 1
                    if listL[itemH] in cannotBeTogether:
                        count = count + 1
                    if count != 2:
                        twoItemsList.append(listL[itemL])
                        twoItemsList.append(listL[itemH])
                        listC2.append(twoItemsList)
    return listC2

def computeF1():
    # STEPS FOR FORMING F1
    for item in listL:
        if (dictionaryI[item] >= dictionaryMIS[item]):
            listF1.append(item)
    printFunction(1 , 0 , listF1)
#    print("Frequent 1-itemsets \n")
#    for item in listF1:
#        print(listOfItems.count(item), ': {', item, '}\n')

if __name__ == "__main__":
    # IMPORT TRANSACTIONS AND OTHER PARAMETERS FROM INPUT TEXT FILES
    with open('input-data.txt', 'r') as f:
        myTransactions = [line.strip() for line in f]
    with open('parameter-file.txt', 'r') as g:
        myParameters = [line.strip() for line in g]
        subString = 'MIS'
        for parameter in myParameters:
            if subString in parameter:
                dictionaryMIS[ parameter[parameter.find('(')+1: parameter.find(')')]] = float((parameter.split('= ',1)[1]))
            elif 'cannot_be_together' in parameter:
                cannotBeTogetherData = parameter.partition('{')[-1].rpartition('}')[0]
                cannotBeTogether = [x.strip() for x in cannotBeTogetherData.split(',')]
            elif 'must-have' in parameter:
                mustHave = parameter.split(': ',1)[1].split(' or ')
            elif 'SDC' in parameter:
                SDC = float(parameter.split('= ',1)[1])
        for transaction in myTransactions:
            transactionList = []
            transaction = transaction.partition('{')[-1].rpartition('}')[0]
            transactionList = [x.strip() for x in transaction.split(',')]
            listOfTrasactions.append(transactionList)
    # SORT THE MIS VALUES AND STORE IN A DICTIONARY
    dictionaryMIS = OrderedDict(sorted(dictionaryMIS.items(), key=lambda t: t[1]))
    #CALL TO THE MAIN ALGORITHM MS-APRIORI
    msApriori()




