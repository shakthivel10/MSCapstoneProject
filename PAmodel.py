import math
import os
import random

dataSetsPath = "./datasets"

def PA(G, sigma, p, q, gamma, SISum):
    n = len(G["V"])

    a = Pr(G, sigma, p, q, gamma)
    b = math.log(math.factorial(n)) + SISum

    return a - b

def SIRange(G, sigma, p, q, gamma, T, s, e):
    n = len(G["V"])

    b = 0
    for i in range(s, e+1):
        b += math.log(selfIter(n, G, sigma, i, p, q, gamma, T))

    return b

def Pr(G, PI, p, q, gamma):
    r = 1 - p - q

    pos, inDeg, outDeg, deg = dict(), dict(), dict(), dict()

    for i in range(len(PI)):
        pos[PI[i]] = i

    logP, logQ, logR = math.log(p), 0, math.log(r)

    if q != 0:
        for i in range(len(PI)):
            inDeg[PI[i]] = 0
            outDeg[PI[i]] = 0
            logQ = math.log(q)

    else:
        for i in range(len(PI)):
            deg[PI[i]] = 0

    m = 0
    res = 0

    if q != 0:
        for i in range(len(PI)):
            newInEdges = 0
            newOutEdges = 0

            PIi = PI[i]
            for vj in G["adj"][PIi]:
                if pos[vj] < pos[PIi]:
                    PIj = vj
                    res += logP
                    if m > 0:
                        res -= math.log(m) - math.log(inDeg[PIj] + gamma)
                    inDeg[PIj] += 1
                    outDeg[PIi] += 1
                    newOutEdges += 1

            for vj in G["adjInv"][PIi]:
                if pos[vj] < pos[PIi]:
                    PIj = vj
                    res += logQ
                    if m > 0:
                        res -= math.log(m) - math.log(outDeg[PIj] + gamma)
                    inDeg[PIi] += 1
                    outDeg[PIj] += 1
                    newInEdges += 1

            m += newOutEdges + gamma

            dPIi = newOutEdges + newInEdges

            if i > 0:
                res += math.log(math.factorial(dPIi)) + logR

    else:
        for i in range(len(PI)):
            newEdges = 0

            PIi = PI[i]
            for vj in G["adj"][PIi]:
                if pos[vj] < pos[PIi]:
                    PIj = vj
                    res += logP
                    if m > 0:
                        res -= math.log(m) - math.log(deg[PIj] + gamma)
                    deg[PIj] += 1
                    deg[PIi] += 1
                    newEdges += 1

            m += newEdges + gamma

            dPIi = newEdges

            if i > 0:
                res += math.log(math.factorial(dPIi)) + logR

    return -res

def Shift(p, v, j):

    arr = p.copy()
    arr.remove(v)
    arr.insert(j, v)

    return arr

def selfIter(n, G, sigma, i, p, q, gamma, T):
    pi = sigma.copy()
    est = 0
    #print("selfiter", i)
    for t in range(1, T+1):
        #print(" t", t)

        vi = random.randint(i, n - 1)
        v = sigma[vi]

        a = [0 for k in range(n - i + 1)]

        for j in range(i, n + 1):
            a[j - i] = Pr(G, Shift(pi, v, j), p, q, gamma)

        mina = min(a)
        l = [k for k in range(i, n + 1)]

        wts = [math.e**-(a[k]-mina) for k in range(len(a))]

        j = random.choices(l, weights=(wts))[0]

        pi = Shift(pi, v, j)

        b = [0 for k in range(n - i + 1)]

        for j in range(i, n + 1):
            b[j - i] = Pr(G, Shift(pi, sigma[i], j), p, q, gamma)

        minb = min(b)

        for j in range(len(b)):
            b[j] -= minb

        for j in range(len(b)):
            b[j] = math.e**(-b[j])

        sumB = sum(b)
        est += b[0]/sumB

    return est/T


def test3(): # Flight Network
    NetworkName = "Flight"
    G = {"V": set([i for i in range(332)])}

    PI, adj, adjInv = list(), dict(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]


    G["adj"] = adj

    print(SIRange(G, PI, 0.87, 0, 0.1, 10000, 0, 25))

def test4(): # Ego Network
    NetworkName = "Ego"
    G = {"V": set([i for i in range(347)])}

    PI, adj = list(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]

    G["adj"] = adj

    print(SIRange(G, PI, 0.94, 0, 0.2, 10000, 0, 30))

def test5(): # Collaboration Network
    NetworkName = "Collaboration"
    G = {"V": set([i for i in range(379)])}

    PI, adj, adjInv = list(), dict(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]

    G["adj"] = adj

    print(SIRange(G, PI, 0.71, 0, 0.1, 10000, 0, 30))


def test6(): # Retweet Network
    NetworkName = "Retweet"
    G = {"V": set([i for i in range(96)])}

    PI, adj, adjInv = list(), dict(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]

    with open("./Processed/AdjInvList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adjInv[arr[0]] = arr[1:]

    G["adj"] = adj
    G["adjInv"] = adjInv

    print(SIRange(G, PI, 0.24, 0.31, 0.1, 1000, 0, 8))

def test7(): # Road Network
    NetworkName = "Road"

    G = {"V": set([i for i in range(2642)])}

    PI, adj = list(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]


    G["adj"] = adj

    print(SIRange(G, PI, 0.56, 0, 0.6, 10000, 0, 100))

def test8(): # Power Grid

    NetworkName = "Power"

    G = {"V": set([i for i in range(4941)])}

    PI, adj = list(), dict()

    with open("./Processed/sorted"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            PI.append(int(line))

    with open("./Processed/AdjList"+NetworkName+"Network.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            adj[arr[0]] = arr[1:]


    G["adj"] = adj

    print(SIRange(G, PI, 0.57, 0, 0.1, 10000, 0, 200))


if __name__ == '__main__':
    test8()
    # main()

