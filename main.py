import input_validation as iv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlim,ylim


class Node:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
    
    def get_dist(self,other):
        finddot = np.array([self.x - other.x,self.y - other.y])
        return np.dot(finddot,finddot)

class Cluster:
    def __init__(self,*args):
        self.cluster = []
        self.name = ""
        for i in args:
            if isinstance(i,Cluster):
                self.cluster += i.cluster
            else:
                self.cluster.append(i)
            self.name += i.name

    def get_dist(self,other,completelinkage):
        dist = np.inf if not completelinkage else - np.inf
        smallestpair = None
        for i in np.arange(len(self.cluster)):
            for j in np.arange(len(other.cluster)):
                ijdist = self.cluster[i].get_dist(other.cluster[j])
                print("Squared distance from " + self.cluster[i].name + " to " + other.cluster[j].name + ": " + str(ijdist))
                dist,smallestpair = get_extreme(smallestpair,dist,ijdist,self.cluster[i],other.cluster[j],completelinkage)
        extreme = "min " if not completelinkage else "max "
        print("\n" + extreme + "squared dist between cluster " + self.name + " and " + other.name + " is between " + smallestpair[0].name + " and " + smallestpair[1].name)
        print()
        return dist


def get_extreme(smallestpair,dist,ijdist,i,j,completelinkage):
        if completelinkage:
            dist = max(dist,ijdist)
        else:
            dist = min(dist,ijdist)
        if dist == ijdist:
            smallestpair = [i,j]
        return dist,smallestpair

def get_data_hypers():
    final_clusters = [Cluster(Node(1,6,"A")),Cluster(Node(1002,20,"B")),Cluster(Node(498,651,"C")),Cluster(Node(6,10,"D")),Cluster(Node(510,622,"E")),\
        Cluster(Node(503,632,"F")),Cluster(Node(4,9,"G")),Cluster(Node(1010,25,"H")),Cluster(Node(1006,30,"I")),Cluster(Node(502,680,"J"))]
    points = np.zeros((len(final_clusters),3))
    getpointidx = {}
    for i in np.arange(len(final_clusters)):
        node = final_clusters[i].cluster[0]
        rowi = [node.x,node.y]
        rowi.append(None)
        points[i] = np.array(rowi)
        getpointidx[node] = i
    return True if iv.validate("Complete linkage (n means single)?") == 'y' else False,iv.validate("Until how many clusters?",cast=int,bool_fxn=iv.check_posint_finite),\
        final_clusters,points,getpointidx

def get_combine(completelinkage,clusters):
    extremeclusterdist = np.inf
    combine = [None,None]
    for i in np.arange(len(clusters)):
        for j in np.arange(1 + i,len(clusters)):
            if i != j:
                ijdist = clusters[i].get_dist(clusters[j],completelinkage)
                extremeclusterdist = min(extremeclusterdist,ijdist)
                if ijdist == extremeclusterdist:
                    combine = [clusters[i],clusters[j]]
    extreme = "smallest " if not completelinkage else "smallest biggest "
    print(extreme + "squared distance between 2 clusters is between cluster " + combine[0].name + " and " + combine[1].name)
    print()
    return combine

def acummulate(combine,clusters):
    clusters.remove(combine[0])
    clusters.remove(combine[1])
    clusters.append(Cluster(combine[0],combine[1]))
    return clusters

def agglomerate(clusters,final_clusternum,completelinkage):
    if final_clusternum >= len(clusters):
        print("Goal number of clusters already achieved or is higher than number of data points")
        return clusters
    for i in np.arange(len(clusters) - final_clusternum):
        combine = get_combine(completelinkage,clusters)
        clusters = acummulate(combine,clusters)
        printable = [None] * len(clusters)
        for i in np.arange(len(clusters)):
            printable[i] = clusters[i].name
        print("Now dealing with " + str(printable))
    return clusters

def color(points,clusters,getpointidx):
    for i in np.arange(len(clusters)):
        for j in np.arange(len(clusters[i].cluster)):
            points[getpointidx[clusters[i].cluster[j]],2] = i
    return points


completelinkage,final_clusternum,final_clusters,points,getpointidx = get_data_hypers()
points = color(points,agglomerate(final_clusters,final_clusternum,completelinkage),getpointidx)
plt.scatter(points[:,0],points[:,1],c=points[:,2])
xlim(min(points[:,0]) - 10,max(points[:,0]) + 10)
ylim(min(points[:,1]) - 10,max(points[:,1]) + 10)
plt.show()
