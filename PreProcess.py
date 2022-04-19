from math import log
import os

path = "./"
dataSetsPath = "./datasets"
def main():
    print(os.getcwd())

    for dataset in os.listdir(dataSetsPath):
        indType = None
        gType = None
        n, m = 0, 0
        D, outD, inD = dict(), dict(), dict()
        adj, adjInv = dict(), dict()

        with open(os.path.join(dataSetsPath, dataset)) as file:

            lines = file.readlines()[0:4]

            indType = lines[0]
            gType = lines[1].strip()
            n = int(lines[2])
            m = int(lines[3])

            if gType == "Directed":
                for i in range(n):
                    outD[i] = 0
                    inD[i] = 0
                    adj[i] = []
                    adjInv[i] = []

            elif gType == "Undirected":
                for i in range(n):
                    D[i] = 0
                    adj[i] = []

            else:
                raise Exception('Graph type is neither Directed or Undirected')


        with open(os.path.join(dataSetsPath, dataset)) as file:
            i = 0
            for line in file:

                if i<4:
                    i += 1
                    continue

                arrn = line.split()[:2]
                if indType[0] == '0':
                    nodes = [int(x) for x in arrn]
                elif indType[0] == '1':
                    nodes = [int(x)-1 for x in arrn]
                else:
                    raise Exception('Invalid IndexType in Graph DataSet')

                if gType == "Directed":
                    outD[nodes[0]] += 1
                    inD[nodes[1]] += 1

                    adj[nodes[0]].append(nodes[1])
                    adjInv[nodes[1]].append(nodes[0])

                elif gType == "Undirected":
                    D[nodes[0]] += 1
                    D[nodes[1]] += 1

                    adj[nodes[0]].append(nodes[1])
                    adj[nodes[1]].append(nodes[0])

                else:
                    raise Exception('Graph type is neither Directed or Undirected')

        if gType == "Directed":
            arr = []

            for i in range(n):
                arr.append([i, outD[i]+inD[i]])

            arr.sort(key=lambda x:x[1], reverse=True)
            # print(arr)

            f = open("./Processed/sorted"+dataset, "w")

            for i in range(len(arr)-1):
                f.write(str(arr[i][0])+'\n')
            f.write(str(arr[-1][0]))
            f.close()

            f = open("./Processed/AdjList"+dataset, "w")

            for i in range(n-1):
                f.write(str(i)+ " ")
                f.writelines(["%s " % item for item in adj[i]])
                f.write("\n")
            f.write(str(n-1) + " ")
            f.writelines(["%s " % item for item in adj[n-1]])
            f.close()

            f = open("./Processed/AdjInvList"+dataset, "w")

            for i in range(n-1):
                f.write(str(i)+ " ")
                f.writelines(["%s " % item for item in adjInv[i]])
                f.write("\n")
            f.write(str(n-1) + " ")
            f.writelines(["%s " % item for item in adjInv[n-1]])
            f.close()

        elif gType == "Undirected":
            arr = []

            for i in range(n):
                arr.append([i, D[i]])

            arr.sort(key=lambda x: x[1], reverse=True)
            # print(arr)

            f = open("./Processed/sorted" + dataset, "w")

            for i in range(len(arr) - 1):
                f.write(str(arr[i][0]) + '\n')
            f.write(str(arr[-1][0]))
            f.close()

            f = open("./Processed/AdjList" + dataset, "w")

            for i in range(n - 1):
                f.write(str(i) + " ")
                f.writelines(["%s " % item for item in adj[i]])
                f.write("\n")
            f.write(str(n - 1) + " ")
            f.writelines(["%s " % item for item in adj[n - 1]])
            f.close()

        else:
            raise Exception('Graph type is neither Directed or Undirected')


if __name__ == '__main__':
    main()