from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_extraction.text import CountVectorizer
from ERtasks.models import Cora_labeled,Cora
from sigirexperiments import  models
from DEXTRA import precluster

def gtIG():
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    clusterids = [item.clusterid for item in cora_true]
    data = [item.cora.text for item in cora_true]
    list_sort_value_desc = IG(data=data,clusterids=clusterids)
    return list_sort_value_desc

def preClusterIG():
    groups = precluster.preclusterTest()
    for d in groups:
        print(d)
        print(d[0])
        ds = Cora.objects.filter(text=d[0])

from sigirexperiments import dextrapreclustering

def minHashFastClusterIG(clusternum,cora,username):
    clustdict = dextrapreclustering.minhashFastClustering(clusternum=clusternum, cora=cora)
    cluster_membership = {}

    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    bb_pred = [v for k, v in cluster_membership.items()]
    data = [item.text for item in cora]
    list_sort_value_desc = IG(data=data,clusterids=bb_pred)
    for k,v in list_sort_value_desc:
        print(k,v)
        if not models.sigirAttrExploration.objects.filter(substring=k,orderscore=v,user=username):
            models.sigirAttrExploration.objects.create(substring=k,orderscore=v,user=username)
    return list_sort_value_desc


def IG(data,clusterids):
    cv = CountVectorizer(max_df=0.95, min_df=2,
                         max_features=10000,
                         stop_words='english')
    X_vec = cv.fit_transform(data)
    res = dict(zip(cv.get_feature_names(),
                   mutual_info_classif(X_vec, clusterids, discrete_features=True)
                   ))
    print(res)
    list_sort_value_desc = precluster.sort_dict(res)
    print(list_sort_value_desc[0:20])
    # for k,v in list_sort_value_desc:
    #     print(k,v)
    #     models.sigirAttrExploration.objects.create(substring=k,orderscore=v)
    return list_sort_value_desc