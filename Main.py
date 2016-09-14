import re
from collections import OrderedDict
from operator import itemgetter

#Input parameter-file values
dictionaryMIS = {}
dictionaryI={}
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
                    if(tailCandidateString in dictionaryTailCount.keys()):
                        dictionaryTailCount[tailCandidateString] = dictionaryTailCount[tailCandidateString] + 1
                    else:
                        dictionaryTailCount[tailCandidateString] = 1
                elif(tailCandidateString not in dictionaryTailCount.keys()):
                    dictionaryTailCount[tailCandidateString] = 0
        listOfC = []
        for c in listCk:
            stringC = ','.join(c)
            if(dictionaryCount[stringC]/len(listOfTrasactions) >= dictionaryMIS[ c[0] ]):
                listOfC.append(c)
        dictionaryFk[k] = listOfC

        printFunction(k, dictionaryTailCount, dictionaryFk[k])
#        print("\ndictionary tail count: ", dictionaryTailCount)
#        print("\nF", k, ": ", dictionaryFk[k])
#        print("END OF ONE ITERATION\n")
        k = k + 1



def msCandidateGen(listFkMinus1):
    #EMPTY THE CANDIDATE LIST Ck
    listCk = []

    for i in range(0,len(listFkMinus1)):
        for j in range(i+1,len(listFkMinus1)):
            flag = 1
            for k in range( 0,len(listFkMinus1[i]) - 1 ):
                if(listFkMinus1[i][k] != listFkMinus1[j][k]):
                    flag = 0
                    break
            if(flag == 1):
                if( dictionaryMIS[listFkMinus1[i][len(listFkMinus1[i]) - 1]] < dictionaryMIS[listFkMinus1[j][len(listFkMinus1[i]) - 1]]) \
                        and (dictionaryI[listFkMinus1[i][len(listFkMinus1[i]) - 1]] - dictionaryI[(listFkMinus1[j][len(listFkMinus1[i]) - 1])] <= SDC):
                    listC = []
                    listC = listFkMinus1[i][:]
                    listC.append(listFkMinus1[j][len(listFkMinus1[i]) - 1])
                    listCk.append(listC)
                    subSetList = []
#DILIP CODE
                    for i in range(0, len(listC)):
                        if (i == 0):
                            for j in range(i + 1, len(listC)):
                                listSub = []
                                listSub.append(listC[i])
                                if (len(listC[i + 1:j]) != 0):
                                    listSub = listSub + listC[i + 1:j]
                                if (len(listC[j + 1:]) != 0):
                                    listSub = listSub + listC[j + 1:]
                                subSetList.append(listSub)
                        else:
                            subSetList.append(listC[i:])
                            break;
                    for subSet in subSetList:
                        if (listC[0] in subSet) or ( dictionaryMIS[listC[1]] == dictionaryMIS[listC[0]] ):
                            if subSet not in listFkMinus1:
                                listCk.remove(listC)
    return listCk

def printFunction(k, dictionaryTailCount , listFk):
    dictionaryFrequency = {}
    if(k == 1):
        print("Frequent 1-itemsets \n")
        for item in listFk:
            print("\t",listOfItems.count(item), ': {', item, '}')
    else:
        print("Frequent ", k,"-itemsets \n")
        for item in listFk:
            itemSubString = ','.join(item[1:])
            itemString =','.join(item)
            dictionaryFrequency = computeFrequency(listFk)
            print("\t",dictionaryFrequency[itemString],": {", itemString, "}")
            print("\tTailcount = ",dictionaryTailCount[itemSubString])
    print("\n\tTotal number of freuqent ",k, "-itemsets = ",len(listFk),"\n")

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
    numberOfTransactions = myTransactions.__len__();
    for transaction in listOfTrasactions:
        for item in transaction:
            listOfItems.append(item)
    setOfItems = set(listOfItems)
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
                cannotBeTogether.append(parameter.split(': ',1)[1])
            elif 'must-have' in parameter:
                mustHave.append(parameter.split(': ',1)[1])
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


