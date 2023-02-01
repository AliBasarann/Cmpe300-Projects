import math
import time
import numpy as np

def func(arr):
    arr2=[0,0,0,0,0]
    n = len(arr)
    for i in range(n):
        if (arr[i] == 0):
            for t1 in range(i,n):
                p1 = math.sqrt(t1)
                x1 = n+1
                while (x1>=1):
                    x1 = int(x1/2)
                    arr2[i%5] = arr2[i%5] + 1
        elif(arr[i] == 1):
            for t2 in range(n,0,-1):
                for p2 in range(1,n+1):
                    x2 = n+1
                    while(x2 > 0):
                        x2 = int(x2/2)
                        arr2[i%5] = arr2[i%5] + 1
        elif(arr[i] == 2):
            for t3 in range(1,n+1):
                x3 = t3 + 1
                for p3 in range(pow(t3,2)):
                    arr2[i%5] = arr2[i%5] + 1
    return arr2

sizes = [1,5,10,25,50,75,100,150,200,250]

for i in range(10):
    start = time.time_ns()
    func([0]*sizes[i])
    end = time.time_ns()
    elapsedTime = end - start
    print("Case: Best Size: {} Elapsed Time: {:.2f}".format( sizes[i],  elapsedTime/1000000))


for i in range(10):
    start = time.time_ns()
    func([2]*sizes[i])
    end = time.time_ns()
    elapsedTime = end - start
    print("Case: Worst Size: {} Elapsed Time: {:.2f}".format( sizes[i],  elapsedTime/1000000))

for i in range(10):
    start = time.time_ns()
    func(np.random.randint(0,3,sizes[i]))
    end = time.time_ns()
    elapsedTime = end - start
    print("Case: Average Size: {} Elapsed Time: {:.2f}".format( sizes[i],  elapsedTime/1000000))
