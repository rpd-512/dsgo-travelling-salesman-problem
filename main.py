from random import randint, shuffle, uniform
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import numpy as np
from math import floor

def generatePaths(pop,size):
    rArr = []
    path = list(range(1,size+1))
    for _ in range(pop):
        pth = path[:]
        shuffle(pth)
        rArr.append(pth)
    print("\n")
    return rArr

def fitness(chrm,distance_matrix):
    fit = 0
    for c in range(len(chrm)):
        fit+=distance_matrix[chrm[c]-1][chrm[c-1]-1]
    return fit

#def crossover(xi,xj,cLen,crsPnt):
    def findPos(lst,val):
        for v,l in enumerate(lst):
            if(l==val):
                return v
        return -1
    xNew=xi[:]
    if(len(xi) != len(xj)):
        raise ValueError("Both chromosomes need to have same length")
    if(cLen > len(xi)):
        raise ValueError("Crossover length can't exceed length of chromosome")
    if(cLen+crsPnt > len(xi)):
        raise ValueError("Crossover point overflowed")
    chromoCross = xj[crsPnt:crsPnt+cLen]
    chromoCross.reverse()
    for i,gene in enumerate(xi):
        in_cross = (i>=crsPnt and i<crsPnt+cLen)
        if(in_cross):
            crosschrm = chromoCross.pop()
            pos = findPos(xi,crosschrm)
            xNew[i], xNew[pos] = xNew[pos],xNew[i]
    return xNew

def crossover(xi,xj,cLen,crsPnt):
    def findPos(lst,val):
        for v,l in enumerate(lst):
            if(l==val):
                return v
        return -1

    if(len(xi) != len(xj)):
        raise ValueError("Both chromosomes need to have same length")
    if(cLen > len(xi)):
        raise ValueError("Crossover length can't exceed length of chromosome")
    if(cLen+crsPnt > len(xi)):
        raise ValueError("Crossover point overflowed")

    xNew = [0]*len(xi)
    buffer_gene = []
    carry_holder = []
    crossChrom = xj[crsPnt:crsPnt+cLen]
    xNew[crsPnt:crsPnt+cLen] = crossChrom
    for i,g in enumerate(xi[crsPnt:crsPnt+cLen]):
        if(g not in crossChrom):
            buffer_gene.append(g)
    for i,g in enumerate(xi):
        if(g not in crossChrom and g not in buffer_gene):
            xNew[i] = g
    xNew = list(np.roll(xNew,len(xNew)-(crsPnt+cLen)))
    buffer_gene.reverse()
    
    for _ in range(xNew.count(0)):
        for i in range(len(xNew)-cLen-1):
            if(xNew[i]==0):
                xNew[i], xNew[i+1] = xNew[i+1], xNew[i]

    for i,g in enumerate(xNew):
        if(g == 0):
            xNew[i] = buffer_gene.pop()

    xNew = list(np.roll(xNew,(crsPnt+cLen)-len(xNew)))
    return xNew


def discreetSocialGroupTSP(popSize,itrnNum,pathArr,distMatrix,pathSize,cLen1,cLen2):
    plotData = []
    plotData.append([[],[]])
    cLen1 = floor(cLen1*pathSize)
    cLen2 = floor(cLen2*pathSize)
    if(itrnNum<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")

    #create generation 0
    popData = []
    for u in range(popSize):
        posArr = pathArr[u]
        popData.append([fitness(posArr,distMatrix),posArr])

    #initiate evolution loop
    popData.sort()
    gbest = popData[0]

    print("Evaluating Discreet Social Group Optimization")
    for gen in tqdm (range(itrnNum+1), desc="Working..."):
        popData.sort()
        if(popData[0][0]<gbest[0]):
            gbest = popData[0]

        plotData[0][0].append(gen)
        plotData[0][1].append(fitness(gbest[1],distMatrix))

        #---improving stage---#
        for popl in range(popSize-1):
            p = popData[popl]
            cLen1_r = floor(cLen1*uniform(.5,1.5))
            nP = crossover(p[1],gbest[1],cLen1_r,randint(0,pathSize-cLen1_r-1))
            popData[popl]=[fitness(nP,distMatrix),nP]
        
        #---aquiring phase---#
        
        for popl in range(popSize-1):
            p = popData[popl]
            rp = popData[randint(0,popSize-1)]
            cLen1_r = floor(cLen1*uniform(.5,1.5))
            cLen2_r = floor(cLen2*uniform(.5,1.5))
            if(p[0]<rp[0]):
                nP = crossover(p[1],popData[randint(0,popSize-1)][1],cLen1_r,randint(0,pathSize-cLen1_r))
                nP = crossover(nP,gbest[1],cLen2_r,randint(0,pathSize-cLen2_r))
            else:
                nP = crossover(popData[randint(0,popSize-1)][1],p[1],cLen1_r,randint(0,pathSize-cLen1_r))
                nP = crossover(nP,gbest[1],cLen2_r,randint(0,pathSize-cLen2_r))
            popData[popl]=[fitness(nP,distMatrix),nP]
        
        #assigning fitness values
        for pd in popData:
            pd[0] = fitness(pd[1],distMatrix)
    while(gbest[1][0] != 1):
        gbest[1] = np.roll(gbest[1],1)
    print("Solution from DSGO:", list(map(int,gbest[1])))
    return plotData


if __name__ == "__main__":
    #----------------------------parameters----------------------------#
    populationSize = 300 #size of population
    iterationNum = 500 #how many iterations
    #DATASET: GR17
    distanceMatrix = [
        [0, 633, 257,  91, 412, 150,  80, 134, 259, 505, 353, 324,  70, 211, 268, 246, 121],
        [633,   0, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
        [257, 390,   0, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142],
        [91, 661, 228,   0, 383, 120,  77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
        [412, 227, 169, 383,   0, 267, 351, 309, 338, 196,  61, 421, 346, 243, 199, 528, 297],
        [150, 488, 112, 120, 267,   0,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
        [80, 572, 196,  77, 351,  63,   0,  29, 232, 444, 292, 297,  47, 150, 207, 332,  29],
        [134, 530, 154, 105, 309,  34,  29,   0, 249, 402, 250, 314,  68, 108, 165, 349,  36],
        [259, 555, 372, 175, 338, 264, 232, 249,   0, 495, 352,  95, 189, 326, 383, 202, 236],
        [505, 289, 262, 476, 196, 360, 444, 402, 495,   0, 154, 578, 439, 336, 240, 685, 390],
        [353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   0, 435, 287, 184, 140, 542, 238],
        [324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   0, 254, 391, 448, 157, 301],
        [70, 567, 191,  27, 346,  83,  47,  68, 189, 439, 287, 254,   0, 145, 202, 289,  55],
        [211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   0,  57, 426,  96],
        [268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   0, 483, 153],
        [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   0, 336],
        [121, 518, 142,  84, 297,  35,  29,  36, 236, 390, 238, 301,  55,  96, 153, 336,   0]
    ]
    pathArray = generatePaths(populationSize,len(distanceMatrix[0]))
    pathLenth = len(distanceMatrix[0])
    cLen1 = 0.5
    cLen2 = 0.4
    #OPTIMAL SOLUTION
    opti_sol_list = [
        1,4,13,7,8,6,17,14,15,3,11,10,2,5,9,12,16
    ]
    #------------------------------------------------------------------#
    
    dsgoData = discreetSocialGroupTSP(populationSize,iterationNum,pathArray,distanceMatrix,pathLenth,cLen1,cLen2)
    dsgoFitData = dsgoData[0]


    plt.figure(figsize=(15,8))
    plt.plot(dsgoFitData[0],dsgoFitData[1],color='y',label='DSGO Algorithm')

    plt.xlabel("Iternation Number")
    plt.ylabel("Fitness value")
    plt.title("DSGO Travelling Salesman Problem\nFitness Value")

    plt.legend()

    
    print("Total Distance (DSGO):",dsgoFitData[1][-1])
    print("Optimal Solution",opti_sol_list)
    print("Total Distance (Optimal)", fitness(opti_sol_list,distanceMatrix))
    plt.show()
    
