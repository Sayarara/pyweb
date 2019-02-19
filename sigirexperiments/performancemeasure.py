#from sklearn.metrics import normalized_mutual_info_score
from sklearn import  metrics
from sigirexperiments import  models

def clusterNMI(y_true,y_pred):
    nmi =metrics.normalized_mutual_info_score(y_true, y_pred)
    return  nmi

def clusterARI(y_true,y_pred):
    ari = metrics.adjusted_rand_score(y_true, y_pred)
    return ari

def clusterAMI(y_true,y_pred):
    ami = metrics.adjusted_mutual_info_score(y_true, y_pred)
    return ami

def clusterMeasureSet(aa_true, bb_pred,RecordSamplingMethod,workerOperationNum):
    nmi = metrics.normalized_mutual_info_score(aa_true, bb_pred)
    ari = metrics.adjusted_rand_score(aa_true, bb_pred)
    ami = metrics.adjusted_mutual_info_score(aa_true, bb_pred)
    homogeneity = metrics.homogeneity_score(aa_true, bb_pred)
    completeness = metrics.completeness_score(aa_true, bb_pred)
    v_measure = metrics.v_measure_score(aa_true, bb_pred)
    fmi = metrics.fowlkes_mallows_score(aa_true, bb_pred)
    dict = {'RecordSamplingMethod':RecordSamplingMethod,'workerOperationNum': workerOperationNum,'nmi':nmi,'ari':ari, 'ami': ami,'homogeneity': homogeneity,'completeness':completeness,'v_measure': v_measure,'fmi': fmi}
    for k,v in dict.items():
      print(k,' ',v)
    for k,v in dict.items():
      print(v)
    return dict


def record_sampling_clustermultimeasure_vs_opnum(wn,samplemth):
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    aa_true = [item.clusterid for item in cora_true]
    cluster_membership = models.CoraPerformanceLog.objects.filter(
        explorationMethod=samplemth, workerOperationNum=wn).order_by(
        'cora_id')
    bb_pred = [item.clusterid for item in cluster_membership]
    nmi = metrics.normalized_mutual_info_score(aa_true, bb_pred)
    ari = metrics.adjusted_rand_score(aa_true, bb_pred)
    ami = metrics.adjusted_mutual_info_score(aa_true, bb_pred)
    homogeneity = metrics.homogeneity_score(aa_true, bb_pred)
    completeness = metrics.completeness_score(aa_true, bb_pred)
    v_measure = metrics.v_measure_score(aa_true, bb_pred)
    fmi = metrics.fowlkes_mallows_score(aa_true, bb_pred)
    dict = {'RecordSamplingMethod': samplemth.name,'workerOperationNum': wn,'nmi':nmi,'ari':ari, 'ami': ami,'homogeneity': homogeneity,'completeness':completeness,'v_measure': v_measure,'fmi': fmi}
    for k,v in dict.items():
      print(k,' ',v)
    return dict

def record_common_cluster_measure(samplemth,list):
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    aa_true = [item.clusterid for item in cora_true]
    # for n in [15,20,25,30,35, 40, 45, 50, 55, 60, 65, 70, 75,80]:
    for n in list:
        cluster_membership = models.CoraPerformanceLog.objects.filter(
            explorationMethod=samplemth, workerOperationNum=n).order_by(
            'cora_id')
        bb_pred = [item.clusterid for item in cluster_membership]
        dict = clusterMeasureSet(aa_true=aa_true, bb_pred=bb_pred,
                                                    RecordSamplingMethod=samplemth,
                                                    workerOperationNum=n)
        f = open('C:/Users/sayarara/Desktop/实验记录/DEXTRARandomSamplingIG/'+str(n)+'.txt', 'a')
        for k, v in dict.items():
            #print(k, ' ', v)
            print(v)
            f.write(str(v)+'\n')
        f.close()
    return 1

def record_search_cluster_measure(samplemth):
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    aa_true = [item.clusterid for item in cora_true]
    for n in [10,20,30, 40, 50, 60, 70, 80]:
        cluster_membership = models.CoraPerformanceLog.objects.filter(
            explorationMethod=samplemth, workerOperationNum=n).order_by(
            'cora_id')
        bb_pred = [item.clusterid for item in cluster_membership]
        dict = clusterMeasureSet(aa_true=aa_true, bb_pred=bb_pred,
                                                    RecordSamplingMethod=samplemth,
                                                    workerOperationNum=n)
        f = open('C:/Users/sayarara/Desktop/实验记录/searchsampling/'+str(n)+'.txt', 'a')
        for k, v in dict.items():
            #print(k, ' ', v)
            print(v)
            f.write(str(v)+'\n')
        f.close()
    return 1

from ERtasks.models import Cora_labeled
from sigirexperiments import dextrapreclustering
def minHashFastClusteringPerformanceMeasure(clusternum):
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    aa_true = [item.clusterid for item in cora_true]
    cora = Cora_labeled.objects.all()
    clustdict=dextrapreclustering.minhashFastClustering(clusternum=clusternum,cora=cora)
    cluster_membership = {}

    for k,v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    bb_pred = [v for k, v in cluster_membership.items()]

    for k, v in cluster_membership.items():
        print(k, v)
    clusterMeasureSet(aa_true=aa_true,bb_pred=bb_pred,RecordSamplingMethod="minhashFastClustering",workerOperationNum=-1)
    return 0
