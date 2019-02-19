from datasketch import MinHash
import fastcluster
from ERtasks.models import Cora_labeled
import affinegap

def minhashFastClustering(clusternum,cora):
    # cora = Cora_labeled.objects.all()
    minhashs = []
    for item in cora:
        m = MinHash(num_perm=128)
        s = set(item.cleantext.split(" "))
        for d in s:
            m.update(d.encode('utf8'))
        minhashs.append(m)

    # distance matric
    dis = []
    for n in range(len(minhashs)):
        row = []
        for i in range(0, len(minhashs)):
            row.append(minhashs[n].jaccard(minhashs[i]))
        dis.append(row)
    linkage = fastcluster.linkage(dis, method="complete")
    # clusternum = 2
    clustdict = {i: [i] for i in range(len(linkage) + 1)}
    for i in range(len(linkage) - clusternum + 1):
        clust1 = int(linkage[i][0])
        clust2 = int(linkage[i][1])
        clustdict[max(clustdict) + 1] = clustdict[clust1] + clustdict[clust2]
        del clustdict[clust1], clustdict[clust2]

    print(clustdict)
    return clustdict

import math
def minhashPreClustering(cora):
    count = cora.count()
    a = math.floor(count / 3)
    clustdict = minhashFastClustering(clusternum=a, cora=cora)
    return clustdict

def affinegapSimpleClustering(data):
    a = math.floor(len(data) / 20)
    clusterdict = affinegapFastClustering(clusternum=a,data=data)
    return clusterdict

def affinegapFastClustering(clusternum,data):
    # distance matric
    dis = []
    for n in range(len(data)):
        row = []
        for i in range(0, len(data)):
            d3 = affinegap.normalizedAffineGapDistance(data[n], data[i])
            row.append(d3)
        dis.append(row)
    linkage = fastcluster.linkage(dis, method="complete")
    # clusternum = 2
    clustdict = {i: [i] for i in range(len(linkage) + 1)}
    for i in range(len(linkage) - clusternum + 1):
        clust1 = int(linkage[i][0])
        clust2 = int(linkage[i][1])
        clustdict[max(clustdict) + 1] = clustdict[clust1] + clustdict[clust2]
        del clustdict[clust1], clustdict[clust2]

    print(clustdict)
    return clustdict

from scipy.cluster.hierarchy import fcluster
def affinegaphClustering(data):
    # distance matric
    print(data)
    dis = []

    for n in range(len(data)):
        row = []
        for i in range(0, len(data)):
            d3 = affinegap.normalizedAffineGapDistance(data[n], data[i])
            row.append(d3)
        dis.append(row)
    print(dis)
    linkage = fastcluster.linkage(dis, method="complete")
    b = fcluster(linkage, t=0.99, criterion='inconsistent')
    print(b)
    return b

