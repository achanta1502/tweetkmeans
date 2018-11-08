def calculateJaccardDistance(A,B):
    inter= list(set(A) & set(B))
    sizeOfIntersection=len(inter)
    union= list(set(A) | set(B))
    sizeOfUnion=len(union)
    return round(1-(float(sizeOfIntersection)/sizeOfUnion),4)