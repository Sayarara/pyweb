import re
import csv
import numpy as np
from DEXTRA import precluster
from ERtasks.models import Cora
from django.db.models import Q
from  baselinealloy  import tfidfcosine,iotools,dbtools



def findingSeeds(df, num, seeds_file):
    ds = df.sample(num)
    ds.to_csv(seeds_file, index=False)
    ss = iotools.readData(seeds_file)
    return ss


def highlightingKeywords(seeds):
    # print(ds.loc[:, 'textual'])
    for row in seeds:
        print(row)
        print(seeds[row]['textual'])
        kw = input('please write 3 unique keywords for this record:')
        seeds[row]['keywords'] = kw.split(',')
        print(kw)
    return seeds


def searchtfidf(seedid,kw, num):
    """String representation.
    seeds：sampled records
    num: the number of nearest records of seeds
    """
    # coras = Cora.objects.all()
    kws = kw.split(',')
    # for k in kw.split(','):
    #     print(k)
    #     coras.filter(text__contains=k)
    coras = Cora.objects.filter(Q(text__icontains=kws[0]) & Q(text__icontains=kws[1]) & Q(text__icontains=kws[2]))
    # for item in coras:
    #     print(item.id, item.text)
    print(len(coras))
    indices_data_id = [item.id for item in coras]
    print(indices_data_id)
    print(indices_data_id.__contains__(seedid))
    ooo = indices_data_id.index(seedid)
    print(ooo)
    data = [item.text for item in coras]
    cosine_similarities = tfidfcosine.tfidfcosine(data, ooo)
    related_docs_indices = cosine_similarities.argsort()[:-1 - num - 1:-1]
    print(related_docs_indices)
    print(cosine_similarities[related_docs_indices])
    aa = [indices_data_id[i] for i in related_docs_indices]
    if aa.__contains__(seedid):
        aa.remove(seedid)
    # dict = {'relatedDocs': coras, 'mostrelatedDocs': aa}
    print(aa)
    relatedcors = Cora.objects.filter(id__in = aa)
    for item in relatedcors:
        print(item.id, item.text)
    return relatedcors


def test(kw,seedid,num):
    ds = {}
    kws = kw.split(',')
    for s in kws:
        print(s)
        dic = dbtools.searchFromMysql(s)
        # dc = dictools.count_dicts(dc, dic)
        ds.update(dic)
    print(ds)
    indices_data_id = [dd for dd in ds]
    print(indices_data_id)
    print(indices_data_id.__contains__(seedid))
    ooo = indices_data_id.index(seedid)
    print(ooo)
    data = [ds[dd] for dd in ds]
    print(data)
    cosine_similarities = tfidfcosine.tfidfcosine(data, ooo)
    related_docs_indices = cosine_similarities.argsort()[:-1 - num - 1:-1]
    print(related_docs_indices)
    print(cosine_similarities[related_docs_indices])
    aa = [indices_data_id[i] for i in related_docs_indices]
    aa.remove(seedid)
    dict = {'relatedDocs':ds,'mostrelatedDocs':aa}
    return dict


def search(seeds, num):
    """String representation.
    seeds：sampled records
    num: the number of nearest records of seeds
    """
    for row in seeds:
        kw = seeds[row]['keywords']
        # strr = seeds[row]['textual']
        ds = {}
        # dc = {}
        for s in kw:
            print(s)
            dic = dbtools.searchFromMysql(s)
            # dc = dictools.count_dicts(dc, dic)
            ds.update(dic)
        indices_data_id = [dd for dd in ds]
        print(indices_data_id)
        print(seeds[row]['ID'])
        rowid = int(seeds[row]['ID'])
        print(indices_data_id.__contains__(rowid))
        ooo = indices_data_id.index(rowid)
        print(ooo)
        data = [ds[dd] for dd in ds]
        cosine_similarities = tfidfcosine.tfidfcosine(data, ooo)
        related_docs_indices = cosine_similarities.argsort()[:-1 - num - 1:-1]
        print(related_docs_indices)
        print(cosine_similarities[related_docs_indices])
        aa = [indices_data_id[i] for i in related_docs_indices]
        aa.remove(rowid)
        seeds[row]['relatedDocs'] = ds
        seeds[row]['mostrelatedDocs'] = aa
        print(seeds[row]['mostrelatedDocs'])
        # for i in aa:
        #     print(ds[i])
    return seeds

def label(seeds):
    for row in seeds:
        print(row)
        print(seeds[row]['textual'])
        ds = seeds[row]['relatedDocs']
        aa = seeds[row]['mostrelatedDocs']
        for i in aa:
            print("ID:%d, textual:%s" %(i,ds[i]))
            judge = input('is this similar (y/n)')
            if judge.strip() == "y":
                print("y")
            else:
                print("n")
    return seeds


def searchmh(kw,seedid,num):
    # coras = Cora.objects.all()
    kws = kw.split(',')
    # for k in kw.split(','):
    #     print(k)
    #     coras.filter(text__contains=k)
    coras = Cora.objects.filter(Q(text__icontains=kws[0])| Q(text__icontains=kws[1])|Q(text__icontains=kws[2]))
    dic = {}
    ss = []
    mhfocused = precluster.mh(Cora.objects.get(id=seedid).text.split(' '))
    for ca in coras:
        mhca = precluster.mh(ca.text.split(' '))
        dic[ca.id] = precluster.mhJC(mhfocused, mhca)
        print(dic[ca.id])
    list_sort_value_desc = precluster.sort_dict(dic)
    print(list_sort_value_desc[15:15 + num])

    for d in list_sort_value_desc[1:1 + num]:
        print(d)
        print(d[0])
        a = Cora.objects.get(id=d[0])
        print(a)
        ss += [a]
    return ss