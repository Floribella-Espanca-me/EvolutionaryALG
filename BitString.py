import math
import random


class BitString:
    def __init__(self,size):
        self.size=size
        self.sequence=[]

    def randomSequence(self,seed):
        random.seed(seed)
        r=0
        for i in range(self.size):
            r = random.random()
            self.sequence.append(int(round(r)))
            random.seed(r)
        return r

    @staticmethod
    def mutate(BitString,seed):
        if len(BitString.sequence)!=BitString.size:
            print('I can\'t mutate, I\'m not even alive yet :(')
            return seed
        else:
            random.seed(seed)
            r=random.random()
            r=r*BitString.size
            t=math.floor(r)
            result=BitString.sequence[:]
            if BitString.sequence[t]==0:
                result[t]=1
            else:
                result[t]=0
            return [result,r]

    def bitDifference(self,BitString):
        if len(BitString.sequence)!=len(self.sequence):
            print('nao tens os minimos')
            return -1
        else:
            zipped_lists=zip(self.sequence,BitString.sequence)
            sum = [x + y for (x, y) in zipped_lists]
            return sum.count(1)

    def bitFitness(self,BitString):
        if len(BitString.sequence)!=len(self.sequence):
            print('nao tens os maximos')
            return -1
        else:
            zipped_lists=zip(self.sequence,BitString.sequence)
            sum = [x + y for (x, y) in zipped_lists]
            return sum.count(0)+sum.count(2)

    @staticmethod
    def makeChild(BitStringF,BitStringM):
        if len(BitStringF.sequence) != len(BitStringM.sequence):
            print('i think we should break up :(')
            return None
        else:
            size=len(BitStringF.sequence)
            child=BitString(size)
            sequence=BitStringF.sequence[0:int(size/2)]+BitStringM.sequence[int(size/2):]
            child.sequence=sequence
            #print(str(sequence))
            return child

    def __str__(self):
        return str(self.sequence)
