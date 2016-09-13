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
listC2 = []


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
    # STEPS FOR FORMING F1
    for item in listL:
        if(dictionaryI[item] >= dictionaryMIS[item]):
            listF1.append(item)
    print("Frequent 1-itemsets \n")
    for item in listF1:
        print(listOfItems.count(item) ,': {', item ,'}\n')

# FUNCTION TO COMPUTE THE LEVEL 2 CANDIDATE GENERATION
def computeC2():
    for itemL in range(0,len(listL)):
        if(dictionaryI[ listL[itemL] ] >= dictionaryMIS[ listL[itemL]] ):
            for itemH in range(itemL+1, len(listL)):
                if(dictionaryI[ listL[itemH] ] >= dictionaryMIS[ listL[itemL] ] ) and ( abs(dictionaryI[listL[itemH]]-dictionaryI[listL[itemL]]) <= SDC ):
                    twoItemsList = []
                    twoItemsList.append(listL[itemL])
                    twoItemsList.append(listL[itemH])
                    listC2.append(twoItemsList)
    print(listC2)

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

    # CALL TO THE INIT_PASS FUNCTION
    init_pass()
    computeC2()