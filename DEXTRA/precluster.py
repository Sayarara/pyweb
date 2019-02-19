from datasketch.minhash import MinHash
from ERtasks.models import Cora
import scipy
import scipy.cluster.hierarchy as  sch
from datasketch.minhash import MinHash
import matplotlib.pylab as  plt
from scipy.spatial.distance import pdist
from  django.db.models import Count

def mh(dd):
    m = MinHash()
    for d in dd:
        m.update(d.encode('utf8'))
    return m

def mhJC(u,v):
    e = u.jaccard(v)
    # print(e)print(e)
    return e

def mh2(data1,data2):
    m1 = MinHash()
    m2 = MinHash()
    for d in  data1:
        m1.update(d.encode('utf8'))
    for d in data2:
        m2.update(d.encode('utf8'))
    return m1.jaccard(m2)


def sort_dict(dict_words):
    keys = dict_words.keys()
    values = dict_words.values()
    list_one = [(key, val) for key, val in zip(keys, values)]
    list_sort_value_desc = sorted(list_one, key=lambda x: x[1], reverse=True) # 按照第一个元素（value）降序排列
    # list_sort_value_asc = sorted(list_one, key=lambda x: x[1], reverse=False)  # 按照第一个元素（value）升序排列
    # list_sort_key_desc = sorted(list_one, key=lambda x: x[0], reverse=True)  # 按照第0个元素（key）降序排列
    # list_sort_key_asc = sorted(list_one, key=lambda x: x[0], reverse=False)  # 按照第0个元素（key）升序
    return list_sort_value_desc


def count_dicts(d1, d2):
    ds = {}.fromkeys((d1.keys()),1)
    for k in d2:
        if ds.get(k):
            ds[k] = ds[k]+1
        else:
            ds[k] = 1
    return ds

def kwset(kw_seeds):
    kwset = set()
    for row in kw_seeds:
        kwset.update(kw_seeds[row]['keywords'])
    return  kwset

def test():
    dic = {'a': 2, 'b': 3, 'c': 1}
    dic2 = {'a': 2, 'b': 3, 'd': 1}
    dic1 = {}
    print(count_dicts(dic, dic2))
    print(count_dicts(dic1, dic2))
    list_sort_value_desc = sort_dict(dic)
    print(sort_dict(dic)[0][0])
    for d in list_sort_value_desc:
        print(d[0])

def testsplit():
    str = "digital,lcd,zoom";
    kw = str.split(',')
    print(kw)
    for s in kw:
        print(s)

def precluster():
    data = Cora.objects.all()
    print(data[0].text)
    points = scipy.randn(20, 4)
    dism = pdist(points, 'euclidean')
    z = sch.linkage(dism, method='single')
    #p = sch.dendrogram(z)
    #plt.show()
    cluster = sch.fcluster(z, t=1)
    print(cluster)
    return cluster

def preclusterTest():
    groups = Cora.objects.values_list("entityurl").annotate(groupSize=Count("id")).order_by("groupSize").reverse()
    return groups

# group by the text
def preclusterExact():
    groups = Cora.objects.values_list("text").annotate(groupSize=Count("id")).order_by("groupSize").reverse()
    return groups

