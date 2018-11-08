def calculateJaccardDistance(A, B):
    inter = list(set(A) & set(B))
    sizeOfIntersection = len(inter)
    union = list(set(A) | set(B))
    sizeOfUnion = len(union)
    return round(1-(float(sizeOfIntersection)/sizeOfUnion), 4)
def implementUpdateCentroid(idList, cluster, tokensList, lengthTokensList, numberOfClusters):
    indices = []
    recomputedCentroidIndex = []
    recomputedCentroid = []
    for i in range(numberOfClusters):
        indices.append([j for j, u in enumerate(cluster) if u == i])
        indx=indices[i]
        if (len(indx) != 0):
            token = [tokensList[idx] for idx in indx]
            distance = [[calculateJaccardDistance(token[i],token[j]) for j in range(len(indx))] for i in range(len(indx))]
            temp = [sum(i) for i in distance];
            recomputedCentroidIndex.append(indx[(temp.index(min([sum(i) for i in distance])))])
    recomputedCentroid = [idList[x] for x in recomputedCentroidIndex]
    return recomputedCentroid