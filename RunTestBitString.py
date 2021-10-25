import time
from matplotlib import pyplot as plt

from BitString import *


def RandomGuessing(seed,runNumber):
    nextseed=seed
    bitSizeList=[2,4,8,12,16,22]
    runTimes=[]
    attempts=[]
    for x in bitSizeList:
        runTimesrun=[]
        attemptsrun=[]
        for r in range(runNumber):
            bitToGuess=BitString(x)
            nextseed=bitToGuess.randomSequence(nextseed)
            guessed=False
            timeStart=time.time()
            guessAttempts=0
            while not guessed:
                randomguess=BitString(x)
                nextseed=randomguess.randomSequence(nextseed)
                guessAttempts+=1
                if(bitToGuess.bitDifference(randomguess)==0):
                    guessed=True
                    timeEnd=time.time()
                    attemptsrun.append(guessAttempts)
                    runtime = (timeEnd - timeStart) * 1000
                    runTimesrun.append(runtime)
        runTimes.append(runTimesrun)
        attempts.append(attemptsrun)

    plotGraph(runTimes, bitSizeList, "AverageRunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "AverageNumberOfAttempts", "BitStringSize")
    #print(str(attempts))



def guessByMutation(seed,size,trynumber):
    nextseed=seed
    start=time.time()
    attempts=0
    bitStringToGuess=BitString(size)
    nextseed=bitStringToGuess.randomSequence(nextseed)
    #print("BitStringToGuess: " + str(bitStringToGuess))
    firstGuess=BitString(size)
    nextseed=firstGuess.randomSequence(nextseed)
    #print("FirstGuess:       " + str(firstGuess))
    guessed=False
    while not guessed and attempts<trynumber:
        exe=BitString.mutate(firstGuess,nextseed)
        nextseed=exe[1]
        attempts+=1
        mutatedSequence = exe[0]
        mutantBitString=BitString(size)
        mutantBitString.sequence=mutatedSequence
        if mutantBitString.bitFitness(bitStringToGuess)>firstGuess.bitFitness(bitStringToGuess):
            firstGuess=mutantBitString
        if firstGuess.bitFitness(bitStringToGuess)==size:
            guessed=True
            #print("easy guess")
            break
            #print("i got it: "+str(firstGuess))
            #print("attempts: "+str(attempts))
    #if not guessed:
    #    print("Final guess:      "+str(firstGuess))
    #    print("nao consegui :(, attempts: "+str(attempts))
    end=time.time()
    return [attempts,((end-start)*1000),nextseed]


def mutationTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 22, 32]
    runTimes = []
    attempts = []
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        for i in range(runNumber):
            exe=guessByMutation(nextseed,x,1000)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
    plotGraph(runTimes, bitSizeList, "AverageRunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "AverageNumberOfAttempts", "BitStringSize")

def mutationPopulationTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 22]
    runTimes = []
    attempts = []
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        for i in range(runNumber):
            exe=populationMutate(nextseed,x)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
    plotGraph(runTimes, bitSizeList, "AverageRunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "AverageNumberOfAttempts(100 Strings Per Attempt)", "BitStringSize")

def childrenTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 22]
    runTimes = []
    attempts = []
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        for i in range(runNumber):
            exe=populationChildrenAndMutate(nextseed,x)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
    plotGraph(runTimes, bitSizeList, "AverageRunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "AverageNumberOfAttempts(100 Strings Per Attempt)", "BitStringSize")

def populationMutate(seed,size):
    attempts=0
    start=time.time()
    nextseed = seed
    bitStringToGuess = BitString(size)
    nextseed = bitStringToGuess.randomSequence(nextseed)
    population=[]
    #print(str(bitStringToGuess))
    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)
    firstpop=firstPopulation(nextseed,size,100)
    nextseed=firstpop[1]
    population=firstpop[0][:]
    stop=False
    totalfitness=0
    while not stop:
        population.sort(key=myfunct,reverse=True)
        if population[0].bitFitness(bitStringToGuess)==size:
            stop=True
            break
        selection=population[:29]
        totalfitnesslist=map(myfunct,selection)
        temp=sum(totalfitnesslist)
        if temp> totalfitness:
            totalfitness=temp
            #print(str(totalfitness))
        else:
            stop=True
            break

        population.clear()
        attempts+=1
        exe=populateByMutation(nextseed,size,100,selection)
        population=exe[0][:]
        nextseed=exe[1]
    end=time.time()
    #print(attempts)
    return [attempts,((end-start)*1000),nextseed]

def populationChildrenAndMutate(seed,size):
    attempts=0
    start=time.time()
    nextseed = seed
    bitStringToGuess = BitString(size)
    nextseed = bitStringToGuess.randomSequence(nextseed)
    population=[]
    #print(str(bitStringToGuess))
    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)
    firstpop=firstPopulation(nextseed,size,100)
    nextseed=firstpop[1]
    population=firstpop[0][:]
    stop=False
    totalfitness=0
    while not stop:
        population.sort(key=myfunct,reverse=True)
        if population[0].bitFitness(bitStringToGuess)==size:
            stop=True
            break
        selection=population[:29]
        totalfitnesslist=map(myfunct,selection)
        temp=sum(totalfitnesslist)
        if temp> totalfitness:
            totalfitness=temp
            #print(str(totalfitness))
        else:
            #totalfitness = temp
            stop=True
            break

        population.clear()
        attempts+=1
        exe1=populateByMutation(nextseed,size,70,selection)
        population=exe1[0][:]
        nextseed=exe1[1]
        exe2=populateByChildren(nextseed,30,selection)
        population=population+exe2[0][:]
        nextseed=exe2[1]
    end=time.time()
    #print(attempts)
    return [attempts,((end-start)*1000),nextseed]


def firstPopulation(seed,size,populationsize):
    population=[]
    nextseed=seed
    for x in range(populationsize):
        citizen=BitString(size)
        nextseed=citizen.randomSequence(nextseed)
        population.append(citizen)
    return [population,nextseed]


def populateByMutation(seed,size,populationsize,initialpopulation):
    nextseed=seed
    population=[]
    for x in range(populationsize):
        indexInSelection = populationsize % 30
        exe = BitString.mutate(initialpopulation[indexInSelection], nextseed)
        nextseed = exe[1]
        baby = BitString(size)
        baby.sequence = exe[0]
        population.append(baby)
    return [population,nextseed]

def populateByChildren(seed,populationsize,initialpopulation):
    nextseed=seed
    population=[]
    for x in range(populationsize):
        random.seed(nextseed)
        parents=random.sample(initialpopulation,k=2)
        nextseed = random.random()
        child=BitString.makeChild(parents[0],parents[1])
        population.append(child)
    return [population,nextseed]




def listavr(list):
    if len(list)!=0:
        return sum(list) / len(list)
    else:
        print("cant average empty list")
        return -1

def plotGraph(listY,listX,nameY,nameX):
    fig, ax = plt.subplots()
    ax.boxplot(listY)
    ax.set_xticklabels(listX)
    plt.xlabel(nameX)
    plt.ylabel(nameY)
    plt.show()




