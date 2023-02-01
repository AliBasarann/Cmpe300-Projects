import random
import sys
import time
sys.setrecursionlimit(10000)
def rearrange(inputlist, lowindex, highindex, pivotposition):
    (inputlist[pivotposition], inputlist[lowindex]) = (inputlist[lowindex], inputlist[pivotposition])
    pivot = inputlist[lowindex]
    rightpos = lowindex
    leftpos = highindex + 1
    while(rightpos  < leftpos):
        rightpos += 1
        while (( inputlist[rightpos] < pivot) and ( rightpos < highindex)):
            rightpos += 1
        leftpos -= 1
        while ((inputlist[leftpos] > pivot) and ( leftpos > lowindex)):
            leftpos -= 1
        if(rightpos < leftpos):
            temp = inputlist[leftpos]
            inputlist[leftpos] = inputlist[rightpos]
            inputlist[rightpos] = temp
    position = leftpos
    inputlist[lowindex] = inputlist[position]
    inputlist[position] = pivot
    return position


def quicksortFirstIndex(inputlist,lowIndex, highIndex):
    if(lowIndex < highIndex):
        pivotpos=lowIndex
        position = rearrange(inputlist,lowIndex,highIndex,pivotpos)
        quicksortFirstIndex(inputlist,lowIndex,position-1)
        quicksortFirstIndex(inputlist,position+1,highIndex)
        return inputlist

def quicksortRandom(inputlist,lowIndex, highIndex):
    if(lowIndex < highIndex):
        pivotpos=random.randint(lowIndex,highIndex)
        position = rearrange(inputlist,lowIndex,highIndex,pivotpos)
        quicksortRandom(inputlist,lowIndex,position-1)
        quicksortRandom(inputlist,position+1,highIndex)
        return inputlist

def quicksortRandomList(inputlist,lowIndex, highIndex):
    if(lowIndex < highIndex):
        pivotpos=lowIndex
        random.shuffle(inputlist)
        position = rearrange(inputlist,lowIndex,highIndex,pivotpos)
        quicksortFirstIndex(inputlist,lowIndex,position-1)
        quicksortFirstIndex(inputlist,position+1,highIndex)
        return inputlist

def findMedian(lst):
    copy = lst.copy()
    copy.sort()
    return(copy[1])


def quicksortMedian(inputlist,lowIndex, highIndex):
    if(lowIndex < highIndex):
        newList = [inputlist[lowIndex], inputlist[highIndex], inputlist[(lowIndex+highIndex)//2]]
        pivot = findMedian(newList)
        pivotpos = 0     
        if pivot == newList[0]:
            pivotpos = lowIndex
        elif pivot == newList[1]:
            pivotpos = highIndex
        elif pivot == newList[2]:
            pivotpos = (lowIndex+highIndex)//2
        position = rearrange(inputlist,lowIndex,highIndex,pivotpos)
        quicksortMedian(inputlist,lowIndex,position-1)
        quicksortMedian(inputlist,position+1,highIndex)
        return inputlist



def takeAverage(lst):
    sum = 0
    for i in range(len(lst)):
        sum+=lst[i]
    return sum/len(lst)
def generateList(n,coefficient,worst):
    lst = []
    for i in range(n):
        lst.append(random.randint(1,coefficient*n))
    if(worst):
        lst.sort()

    return lst

#takes number of elements, range of the elements as the first and the second input
#the boolean element in the third parameter shows whether the input is sorted or not sorted
average= generateList(10000,10,False)
worst=generateList(10000,10,True)
start = time.time()
output = quicksortFirstIndex(average,0,len(average)-1)
stop = time.time()
print("Execution time for average input with version1:",stop-start)

start = time.time()
output = quicksortFirstIndex(worst,0,len(worst)-1)
stop = time.time()
print("Execution time for worst input with version1:",stop-start)

start = time.time()
output = quicksortRandom(average,0,len(average)-1)
stop = time.time()
print("Execution time for average input with version2:",stop-start)

start = time.time()
output = quicksortRandom(worst,0,len(worst)-1)
stop = time.time()
print("Execution time for worst input with version2:",stop-start)

start = time.time()
output = quicksortRandomList(average,0,len(average)-1)
stop = time.time()
print("Execution time for average input with version3:",stop-start)

start = time.time()
output = quicksortRandomList(worst,0,len(worst)-1)
stop = time.time()
print("Execution time for worst input with version3:",stop-start)

start = time.time()
output = quicksortMedian(average,0,len(average)-1)
stop = time.time()
print("Execution time for average input with version4:",stop-start)

start = time.time()
output = quicksortMedian(worst,0,len(worst)-1)
stop = time.time()
print("Execution time for worst input with version4:",stop-start)