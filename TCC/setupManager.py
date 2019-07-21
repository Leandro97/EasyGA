import setup
import random as rd

setupList = []

def createSetups(quantity):
    seed = rd.randint(0, 10000)

    for i in range(quantity):
        newSetup = setup.Setup(seed)
        setupList.append(newSetup)

    return setupList

def deleteSetup(setupList, index):
    del setupList[index]
    return setupList