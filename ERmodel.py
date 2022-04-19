from math import log
import os

dataSetsPath = "./datasets"


def MaximumLikelihoodUndirected(n, m):

    e1 = m
    e2 = n*(n-1)-m

    p = m / (n*(n-1))
    res = -1 * (e1 * log(p) + e2 * log(1-p))
    return res


def MaximumLikelihoodDirected(n, m):

    e1 = m
    e2 = n*(n-1)/2-m

    p = 2*m / (n*(n-1))

    res = -1 * (e1 * log(p) + e2 * log(1-p))

    return res


def main():
    print("ER Model")
    for dataset in os.listdir(dataSetsPath):

        print("  Network:" + dataset.split(".")[0])

        with open(os.path.join(dataSetsPath, dataset)) as file:

            lines = file.read().split('\n')

            graphType = lines[1]
            n = float(lines[2])
            m = float(lines[3])

            if graphType == "Directed":
                logLikelihood = MaximumLikelihoodDirected(n, m)
                print("   LogLikelihood: " + str(logLikelihood) + " LogLikelihoodPerEdge: " + str(logLikelihood/m))

            elif graphType == "Undirected":
                logLikelihood = MaximumLikelihoodUndirected(n, m)
                print("    LogLikelihood: " + str(logLikelihood) + " LogLikelihoodPerEdge: " + str(logLikelihood/m))
            else:
                raise Exception('Graph type is neither Directed or Undirected')


if __name__ == '__main__':
    main()