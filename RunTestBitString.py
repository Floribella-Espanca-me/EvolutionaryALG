import time
from matplotlib import pyplot as plt

from BitString import *


def RandomGuessing(seed,runNumber):
    nextseed=seed
    bitSizeList=[2, 4, 8, 12, 16]
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

    plotGraph(runTimes, bitSizeList, "RunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "NumberOfAttempts", "BitStringSize")
    #print(str(attempts))



def guessByMutation(seed,size,trynumber):
    nextseed=seed
    start=time.time()
    attempts=0
    bitStringToGuess=BitString(size)
    nextseed=bitStringToGuess.randomSequence(nextseed)
    firstGuess=BitString(size)
    nextseed=firstGuess.randomSequence(nextseed)
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
            break

    end=time.time()
    return [attempts,((end-start)*1000),nextseed]



def mutationTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 32, 64]
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
    plotGraph(runTimes, bitSizeList, "RunTime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "NumberOfAttempts", "BitStringSize")

def mutationPopulationTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 32, 64]
    runTimes = []
    attempts = []
    attemptsOfSolved=[]
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        attemptsOfSolvedThisSize = []
        for i in range(runNumber):
            exe=populationMutate(nextseed,x)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
            attemptsOfSolvedThisSize.append(exe[3])
        while -1 in attemptsOfSolvedThisSize: attemptsOfSolvedThisSize.remove(-1)
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
        attemptsOfSolved.append(attemptsOfSolvedThisSize)
    plotGraph(runTimes, bitSizeList, "Runtime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "Number of Generations until stagnation", "BitStringSize")
    plotGraph(attemptsOfSolved, bitSizeList, "Generations to Find Solution ", "BitStringSize")

def childrenTester(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 32, 64]
    runTimes = []
    attempts = []
    attemptsOfSolved = []
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        attemptsOfSolvedThisSize = []
        for i in range(runNumber):
            exe=populationChildren(nextseed,x)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
            attemptsOfSolvedThisSize.append(exe[3])
        while -1 in attemptsOfSolvedThisSize: attemptsOfSolvedThisSize.remove(-1)
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
        attemptsOfSolved.append(attemptsOfSolvedThisSize)
    plotGraph(runTimes, bitSizeList, "Runtime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "Number of Generations until stagnation", "BitStringSize")
    plotGraph(attemptsOfSolved, bitSizeList, "Generations to Find Solution", "BitStringSize")

def childrenTesterBADAPROACH(seed,runNumber):
    nextseed = seed
    bitSizeList = [2, 4, 8, 12, 16, 32, 64]
    runTimes = []
    attempts = []
    attemptsOfSolved = []
    for x in bitSizeList:
        runTimethissize=[]
        attemptsThissize=[]
        attemptsOfSolvedThisSize = []
        for i in range(runNumber):
            exe=populationChildrenBADAPROACH(nextseed,x)
            nextseed=exe[2]
            runTimethissize.append(exe[1])
            attemptsThissize.append(exe[0])
            attemptsOfSolvedThisSize.append(exe[3])
        while -1 in attemptsOfSolvedThisSize: attemptsOfSolvedThisSize.remove(-1)
        runTimes.append(runTimethissize)
        attempts.append(attemptsThissize)
        attemptsOfSolved.append(attemptsOfSolvedThisSize)
    plotGraph(runTimes, bitSizeList, "Runtime(ms)", "BitStringSize")
    plotGraph(attempts, bitSizeList, "Number of Generations until stagnation", "BitStringSize")
    plotGraph(attemptsOfSolved, bitSizeList, "Generations to Find Solution", "BitStringSize")

def populationMutate(seed,size):
    attempts=0
    start=time.time()
    nextseed = seed
    bitStringToGuess = BitString(size)
    nextseed = bitStringToGuess.randomSequence(nextseed)
    attemptOfSolved=-1
    solved=False
    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)
    firstpop=firstPopulation(nextseed,size,100)
    nextseed=firstpop[1]
    population=firstpop[0][:]
    olderPopulation=population[:29]
    stagnationflag=0
    while stagnationflag<3:
        population.sort(key=myfunct,reverse=True)
        selection=population[:29]
        if stagnationFlag(olderPopulation,selection,bitStringToGuess):
            stagnationflag+=1
        if myfunct(population[0])==size and not solved:
            attemptOfSolved=attempts
            solved=True
        olderPopulation=selection[:]
        population.clear()
        attempts+=1
        exe=populateByMutation(nextseed,size,70,selection)
        population=selection+exe[0][:]
        nextseed=exe[1]
    end=time.time()
    return [attempts,((end-start)*1000),nextseed,attemptOfSolved]

def populationChildren(seed,size):
    attempts = 0
    start = time.time()
    nextseed = seed
    bitStringToGuess = BitString(size)
    nextseed = bitStringToGuess.randomSequence(nextseed)
    attemptOfSolved = -1
    solved = False

    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)

    firstpop = firstPopulation(nextseed, size, 100)
    nextseed = firstpop[1]
    population = firstpop[0][:]
    olderPopulation = population[:29]
    stagnationflag = 0
    while stagnationflag < 3:
        population.sort(key=myfunct, reverse=True)
        selection = population[:29]
        if stagnationFlag(olderPopulation, selection, bitStringToGuess):
            stagnationflag += 1
        if myfunct(population[0])==size and not solved:
            attemptOfSolved = attempts
            solved = True
        olderPopulation = selection[:]
        population.clear()
        attempts += 1
        exe = populateByChildren(nextseed, 70, selection)
        population = selection + exe[0][:]
        nextseed = exe[1]
    end = time.time()
    # print(attempts)
    return [attempts, ((end - start) * 1000), nextseed, attemptOfSolved]

def populationChildrenBADAPROACH(seed,size):
    attempts = 0
    start = time.time()
    nextseed = seed
    bitStringToGuess = BitString(size)
    nextseed = bitStringToGuess.randomSequence(nextseed)
    attemptOfSolved = -1
    solved = False

    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)

    firstpop = firstPopulation(nextseed, size, 100)
    nextseed = firstpop[1]
    population = firstpop[0][:]
    olderPopulation = population[:29]
    stagnationflag = 0
    while stagnationflag < 3:
        population.sort(key=myfunct, reverse=True)
        selection = population[:29]
        if stagnationFlag(olderPopulation, selection, bitStringToGuess):
            stagnationflag += 1
        if myfunct(population[0])==size and not solved:
            attemptOfSolved = attempts
            solved = True
        olderPopulation = selection[:]
        population.clear()
        attempts += 1
        exe = populateByChildrenBADAPROACH(nextseed, 70, selection)
        population = selection + exe[0][:]
        nextseed = exe[1]
    end = time.time()
    # print(attempts)
    return [attempts, ((end - start) * 1000), nextseed, attemptOfSolved]

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
        child=BitString.makeChild(parents[0],parents[1],nextseed)
        population.append(child[0])
        nextseed=child[1]
    return [population,nextseed]

def populateByChildrenBADAPROACH(seed,populationsize,initialpopulation):
    nextseed=seed
    population=[]
    for x in range(populationsize):
        random.seed(nextseed)
        parents=random.sample(initialpopulation,k=2)
        nextseed = random.random()
        child=BitString.makeChildBADAPROACH(parents[0],parents[1])
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


def stagnationFlag(olderPopulation,youngerPopulation,bitStringToGuess):
    def myfunct(bitstring):
        return bitstring.bitFitness(bitStringToGuess)
    youngerList=map(myfunct,youngerPopulation)
    youngerFitness=sum(youngerList)
    olderList = map(myfunct, olderPopulation)
    olderFitness = sum(olderList)
    if youngerFitness<=olderFitness:
        return True
    else:
        return False


