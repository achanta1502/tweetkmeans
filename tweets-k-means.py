import sklearn as sk
import pandas as pd
from urllib.request import Request, urlopen
import sys, json
import numpy as np
import math

class K_Means:

    def __init__(self, k =25, seedFile = None, tweetDataFile=None, outputFile=None):
        self.k = k
        self.seedFile = seedFile
        self.tweetDataFile = tweetDataFile
        self.outputFile = outputFile

        self.main_function()


    def calculateJaccardDistance(self, a, b):
        inter = list(set(a) & set(b))
        sizeOfIntersection = len(inter)
        union = list(set(a) | set(b))
        sizeOfUnion = len(union)
        return round(1 - (float(sizeOfIntersection) / sizeOfUnion), 4)


    def main_function(self):

        req = Request(self.tweetDataFile,headers={'User-Agent': 'Mozilla/5.0'})
        tweet_data = pd.read_json(urlopen(req).read(), orient="records", lines=True)

        # for index,row in tweet_data.iterrows():
        #     print(row)

        req1 = Request(self.seedFile,headers={'User-Agent': 'Mozilla/5.0'})
        centroid_ids = pd.read_table(urlopen(req1), sep=",", header=None)
        centroid_ids = centroid_ids[0]

        centroids = []
        for i in centroid_ids:
            centroids.append(int(i))

        for i in range(self.k):
            # find the distance between the point and cluster; choose the nearest centroid
            cluster = {}
            for i in range(self.k):
                cluster[i] = []

            centroiddata = {}
            for centroid in centroids:
                for index, row in tweet_data.iterrows():
                    if centroid == int(row['id']):
                        centroiddata[centroid] = row


            for index, features in tweet_data.iterrows():

                distances = [self.calculateJaccardDistance(features['text'], centroiddata[centroid]['text']) for centroid in centroids]
                classification = distances.index(min(distances))
                cluster[classification].append(features['id'])


            for classification in cluster:
                sum = 0
                count = 0

                count1 = 0
                for k in cluster[classification]:
                    if k in centroids and count1 != 1:
                        centroids.remove(k)
                        count1 += 1

                    sum += k
                    count += 1

                if count > 1:
                    val = sum/count
                    mindifference = math.inf
                    id = 0
                    for k in cluster[classification]:
                        val1 = abs(val-k)
                        if val1 < mindifference:
                            mindifference = val1
                            id = k

                    centroids.append(id)


        file = open(self.outputFile,'w')
        file.write("cluster-id" + "\t" + "List of tweet ids separated by comma\n")
        for i in cluster:
            file.write(str(i)+"\t"+str(cluster[i])+"\n")
        file.close()

if __name__ == "__main__":
    k_means_object = K_Means(int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])

