import math
import os
import random

dataSetsPath = "./datasets"

def SmallWorld(G, a, b, T0, R, delta, gt):
    T = T0

    n = len(G["V"])
    s = math.ceil(math.sqrt(n))

    grid = [[None for j in range(s)] for i in range(s)]

    V = G["V"]
    random.shuffle(V)

    for i in range(len(V)):
        grid[i // s][i % s] = V[i]

    xc, yc = dict(), dict()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            xc[grid[i][j]] = i
            yc[grid[i][j]] = j

    currPr = Pr(G, a, b, gt, xc, yc)

    while True:
        r = 0
        while r <= R:
            r += 1
            ux = random.randint(0, s-1)
            uy = random.randint(0, s-1)
            vx = random.randint(0, s-1)
            vy = random.randint(0, s-1)
            u = grid[ux][uy]
            v = grid[vx][vy]

            if u and v:
                newPr = PRcalc(G, grid, ux, uy, vx, vy, currPr, a, b, gt, xc, yc)

                if currPr > newPr:
                    currPr = newPr
                    grid[ux][uy], grid[vx][vy] = grid[vx][vy], grid[ux][uy]
                    xc[u] = vx
                    yc[u] = vy
                    xc[v] = ux
                    yc[v] = uy
                    continue

                p = min(1, (math.e**((currPr-newPr)/T)))

                l = [True, False]
                draw = random.choices(l, weights=([p, 1-p]))

                if draw[0]:
                    currPr = newPr
                    grid[ux][uy], grid[vx][vy] = grid[vx][vy], grid[ux][uy]
                    xc[u] = vx
                    yc[u] = vy
                    xc[v] = ux
                    yc[v] = uy

        T *= (1-delta)

        if T < 1:
            return currPr


def PRcalc(G, oldGrid, ux, uy, vx, vy, currPr, a, b, gt, oldxc, oldyc):
    n = len(G["V"])

    res = currPr
    u = oldGrid[ux][uy]
    v = oldGrid[vx][vy]

    if gt == 1:
        for j in range(n):
            xcu = oldxc[u]
            ycu = oldyc[u]

            if j != v and j != u:
                dist = abs(xcu - oldxc[j]) + abs(ycu - oldyc[j])
                if G["adjMatrix"][u][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][j][u]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][v][j]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][j][v]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))

        for j in range(n):
            xcv = oldxc[v]
            ycv = oldyc[v]

            if j != v and j != u:
                dist = abs(xcv - oldxc[j]) + abs(ycv - oldyc[j])
                if G["adjMatrix"][v][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][j][v]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][u][j]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][j][u]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))



    elif gt == 0:
        for j in range(n):
            xcu = oldxc[u]
            ycu = oldyc[u]

            if j != v and j != u:
                dist = abs(xcu - oldxc[j]) + abs(ycu - oldyc[j])
                if G["adjMatrix"][u][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][v][j]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))


        for j in range(n):
            xcv = oldxc[v]
            ycv = oldyc[v]

            if j != v and j != u:
                dist = abs(xcv - oldxc[j]) + abs(ycv - oldyc[j])
                if G["adjMatrix"][v][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

                if G["adjMatrix"][u][j]:
                    res -= math.log(a) - b * math.log(dist)

                else:
                    res -= math.log((1 - a * (dist ** (-b))))

    else:
        raise Exception('Graph type is neither Directed or Undirected')

    return res



def Pr(G, a, b, gt, xc, yc):
    n = len(G["V"])

    res = 0

    if gt == 1:
        for i in range(n):

            xci = xc[i]
            yci = yc[i]
            for j in range(n):

                if i == j:
                    continue

                dist = abs(xci - xc[j]) + abs(yci - yc[j])

                if G["adjMatrix"][i][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    res += math.log((1 - a * (dist ** (-b))))

    elif gt == 0:
        for i in range(n):

            xci = xc[i]
            yci = yc[i]
            for j in range(i+1, n):

                dist = abs(xci - xc[j]) + abs(yci - yc[j])

                if G["adjMatrix"][i][j]:
                    res += math.log(a) - b * math.log(dist)

                else:
                    p = 1 - a * (dist ** (-b))
                    if p > 0:
                        res += math.log(p)
                    else:
                        print("p <= 0")
                        res -= float("inf")

    else:
        raise Exception('Graph type is neither Directed or Undirected')

    return -res

def test3(): #FlightNetwork

    V = list()
    with open("./Processed/sortedFlightNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}

    adjMatrix = [[False for i in range(332)] for i in range(332)]

    with open("./Processed/AdjListFlightNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True
                adjMatrix[arr[i]][arr[0]] = True
    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.043, 0.05, 1000, 100000, 0.01, 0)

    print(res)


def test4(): #SocialNetwork
    V = list()
    with open("./Processed/sortedEgoNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}

    adjMatrix = [[False for i in range(347)] for i in range(347)]

    with open("./Processed/AdjListEgoNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True
                adjMatrix[arr[i]][arr[0]] = True

    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.045, 0.03, 1000, 100000, 0.01, 0)

    print(res)


def test5(): #CollaborationNetwork
    V = list()
    with open("./Processed/sortedCollaborationNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}

    adjMatrix = [[False for i in range(379)] for i in range(379)]

    with open("./Processed/AdjListCollaborationNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True
                adjMatrix[arr[i]][arr[0]] = True

    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.013, 0.01, 1000, 100000, 0.01, 0)

    print(res)


def test6(): # Retweet Network

    adjMatrix = [[False for i in range(96)] for i in range(96)]

    V = list()
    with open("./Processed/sortedRetweetNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}

    with open("./Processed/AdjListRetweetNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True

    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.019, 0.02, 1000, 100000, 0.01, 1)

    print(res)


def test7(): # Road Network

    adjMatrix = [[False for i in range(2642)] for i in range(2642)]
    V = list()
    with open("./Processed/sortedRoadNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}
    with open("./Processed/AdjListRoadNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True
                adjMatrix[arr[i]][arr[0]] = True

    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.008, 0.63, 1000, 100000, 0.01, 0)
    print(res)


def test8(): # Power Grid

    adjMatrix = [[False for i in range(4941)] for i in range(4941)]
    V = list()
    with open("./Processed/sortedPowerNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            V.append(int(line))

    G = {"V": V}
    with open("./Processed/AdjListPowerNetwork.txt") as file:
        lines = file.read().split('\n')
        for line in lines:
            arr = line.split()
            arr = [int(arr[i]) for i in range(len(arr))]
            for i in range(1, len(arr)):
                adjMatrix[arr[0]][arr[i]] = True
                adjMatrix[arr[i]][arr[0]] = True

    G["adjMatrix"] = adjMatrix

    res = SmallWorld(G, 0.002, 0.35, 1000, 100000, 0.01, 0)

    print(res)

if __name__ == '__main__':
    test8()
    # main()
