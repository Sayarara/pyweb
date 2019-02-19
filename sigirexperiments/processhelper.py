from  DEXTRA import precluster
from ERtasks.models import Cora, Cora_labeled
import re
from django.db.models import Q

def str2list(str):
    c = str.replace('[', '').replace(']', '').split(',')
    print(c)
    d = [int(item) for item in c]
    print(d)
    return d


def simpleAutoMatchDection(temp_d):
    examples = {'distinct': [], 'match': []}
    # got precluster result to create match
    groups = precluster.preclusterExact()
    for d in groups:
        print(d)
        print(d[0])
        if d[1] < 2:
            print(d[1])
            break
        ds = Cora.objects.filter(text=d[0])
        for n in range(len(ds)):
            for i in range(0, n):
                d1 = temp_d[ds[n].id]
                d2 = temp_d[ds[i].id]
                record_pair = (d1, d2)
                examples['match'].append(record_pair)

    # print(groups)
    # co = [d[0] for d in groups[:num]]
    # print(co)
    # create distinct
    count = 0
    while count < 20:
        randpair = Cora.objects.order_by('?')[:2]
        if simpleSetSimilarity(randpair[0].text, randpair[1].text) < 0.1:
            d1 = temp_d[randpair[0].id]
            d2 = temp_d[randpair[1].id]
            record_pair = (d1, d2)
            print(record_pair)
            examples['distinct'].append(record_pair)
            count = count + 1
    return examples

# containment
def simpleSetSimilarity(text1,text2):
    d1 = text1.split(" ")
    d2 = text2.split(" ")
    set1 = set(d1)
    set2 = set(d2)
    inter = set1.intersection(set2)
    m = min(len(set1), len(set2))
    return len(inter) / m

# jaccard
def simpleJaccardSimilarity(text1,text2):
    d1 = text1.split(" ")
    d2 = text2.split(" ")
    set1 = set(d1)
    set2 = set(d2)
    inter = set1.intersection(set2)
    deli = set1.union(set2)
    return len(inter) / len(deli)

def testre(str):
    llist = Cora_labeled.objects.filter(
        Q(text__icontains=' ' + str + ' ') | Q(text__icontains='(' + str + ')') | Q(
            text__icontains='.' + str + ' ') | Q(text__icontains='-' + str + ' '))
    for item in llist:
        print(item.id,item.text)


def simpledatacleaning(text):
    aaa = re.sub('[^a-zA-Z0-9\']', ' ', text)
    aaa = re.sub('  +', ' ', aaa)
    return aaa

from sigirexperiments import  models
from pyweb import dxaconstants
import json
def sos(attrsynonym,taskc,user,samplemth):
    print(attrsynonym)
    corasyno = models.sigirCoraValueSynonym.objects.get(synonym=attrsynonym)
    value = corasyno.value.value
    print(value)
    attra = corasyno.value.attr
    print(attra.attrname)
    llist = Cora_labeled.objects.filter(labeledtext__icontains=attrsynonym)
    # restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
    restr = '<span class = "detailtext">' + attrsynonym + '<span class="deli">|</span><span class="summaryText">' + attra.attrname + '.' + value + '</span></span>'
    for entiy in llist:
        entiy.labeledtext = entiy.labeledtext.replace(attrsynonym, restr)
        entiy.save()
        models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno)
    item = models.sigirAttrExploration.objects.get(substring=value)
    item.is_labelled = True
    item.save()
    msg = {"attrname": attra.attrname, "value": value, "synonym": attrsynonym}
    models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                      optype=dxaconstants.WorkerOperation.valueBind, user=user,
                                      samplingMethod=samplemth)


import json
def storeTrasingData(outputpath,data):
    f = open(outputpath, 'a')
    for item in data:
        f.writelines(json.dumps(data[item]) + '\n')
    f.close()
    return 0

import numpy as np
def exponential_decay(t, init=0.8, m=30, finish=0.2):
    alpha = np.log(init / finish) / m
    l = - np.log(init) / alpha
    decay = np.exp(-alpha * (t + l))
    return decay

def linear_dcay(t,alpha):
    return alpha**t


def list2str(seedslist,deli):
    return deli.join(seedslist)

def str2list(seedstr,deli):
    return seedstr.split(deli)

from sigirexperiments import patternRecommendation
def test(dataset,username,userid):
    matches = []
    seeds = models.patternSeedTemp.objects.filter(user=username)
    attrname = ''
    if seeds:
        seedslist = str2list(seedstr=seeds[0].seedsubstring, deli='###')
        syn = models.sigirCoraValueSynonym.objects.filter(synonym=seedslist[0], userid=15)[0]
        attrname = syn.value.attr.attrname
        print(attrname)
        attrid = syn.value.attr_id
        print(attrid)
        values = models.sigirCoraAttrValue.objects.filter(attr_id=attrid, userid=userid)
        print(item.value for item in values)
        osysn = models.sigirCoraValueSynonym.objects.filter(value_id__in=[item.id for item in values])
        print(item.synonym for item in osysn)
        match = patternRecommendation.findCandidateSilbings(seedslist=seedslist, data=dataset)
        matches = list(set(match).difference(set([item.synonym for item in osysn])))
        print(matches)



def datasetfilteringMultiContitiion(dataset,substring):
    llist = dataset.filter(
        Q(cleantext__icontains=' ' + substring + ' ') | Q(cleantext__istartswith=substring + ' ') | Q(
            cleantext__iendswith=' ' + substring))

    if len(llist) == 0:
        llist = dataset.filter(text__icontains=substring)
    return llist

def viewhelper(substring,attrbute_name,value):
    return '<span class = "detailtext">' + substring + '<span class="deli">|</span><span class="summaryText">' + attrbute_name + '.' + value + '</span></span>'



def getNumofCommonSubstr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum


def createUpdatePatternSeed(username,seedsstr,coraattr):
    ss = models.patternSeedTemp.objects.filter(user=username)
    if ss:
        ss[0].seedsubstring = seedsstr
        ss[0].save()
    else:
        models.patternSeedTemp.objects.create(seedsubstring=seedsstr, user=username)
    dd= models.sigirSynonymsSeedTemp.objects.filter(user=username)
    if dd:
        dd[0].cattr  = coraattr
        dd[0].save()
    else:
        models.sigirSynonymsSeedTemp.objects.create(cattr=coraattr, user=username)
    return 1

def updateUVDcontent(dataset,attra,valueid,attrsynonym,userid,username):
    corasyno = models.sigirCoraValueSynonym(value_id=valueid, synonym=attrsynonym, userid=userid)
    corasyno.save()
    standvalue = corasyno.value.value
    llist = datasetfilteringMultiContitiion(dataset=dataset, substring=attrsynonym)
    restr = viewhelper(substring=attrsynonym, attrbute_name=attra.attrname, value=standvalue)
    for entiy in llist:
        ss = '.'.join([attra.attrname,standvalue])
        if ss not in entiy.labeledtext:
            entiy.labeledtext = entiy.labeledtext.replace(attrsynonym, restr)
            entiy.save()
            models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno,user=username)
    item = models.sigirAttrExploration.objects.filter(substring=attrsynonym, user=username)
    if item:
        item[0].is_labelled = True
        item[0].save()
    msg = {"attrname": attra.attrname, "value": standvalue, "synonym": attrsynonym}
    return msg

def fulfillRecordBufferPool(clustdict,BP_size):
    cluster_stats = {}
    for k, v in clustdict.items():
        for d in v:
            cluster_stats[k] = len(v)

    list_sort_value_desc = precluster.sort_dict(cluster_stats)
    BP = []
    for k,v in list_sort_value_desc[0:BP_size]:
        print(k,v)
        BP.append(clustdict[k][0])
    return BP

def writeTraingTest(path,list):
    f = open(path, 'a')
    for item in list:
        # print(k, ' ', v)
        print(item)
        f.write(item + '\n')
    f.close()


def preocessPredictedResult(path):
    dict = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            a = json.loads(line)
            words = a['words']
            tags = a['tags']
            print(words)
            print(tags)
            for i in range(len(tags)):
                if tags[i] == 'NULL':
                    continue
                if len(words[i]) > 1:
                    if tags[i] not in dict.keys():
                        dict[tags[i]] = [words[i]]
                    else:
                        dict[tags[i]].append(words[i])

    return dict

def filterPredictedResult(dict,userid):
    for key in dict.keys():
        attr = models.sigirCoraAttr.objects.filter(userid=userid,attrname=key)
        if attr:
            values = models.sigirCoraAttrValue.objects.filter(attr_id=attr[0].id)
            syns = models.sigirCoraValueSynonym.objects.filter(value_id__in=[value.id for value in values])
            dict[key] = list(set(dict[key]).difference([syn.synonym for syn in syns]))
    return dict

import fileinput
def writeAllenNLPTestFormat(allennlptestpath,originalpath):
    f = open(allennlptestpath, 'a')
    for line in fileinput.input(originalpath):
        print(line)
        dict = {"sentence": line}
        f.write(json.dumps(dict) + '\n')
    f.close()


def aaa(path):
    dict = {}
    with open(path,
              'r') as f:
        lines = f.readlines()
        for line in lines:
            a = json.loads(line)
            words = a['words']
            tags = a['tags']
            # print(words)
            # print(tags)
            for i in range(len(tags)):
                if len(words[i]) > 3:
                    if tags[i] not in dict.keys():
                        dict[tags[i]] = [words[i]]
                    else:
                        dict[tags[i]].append(words[i])

    t = []
    for k, v in dict.items():
        dict[k] = set(v)
        print(k, dict[k])
        if k == 'NULL' or k == 'ooo':
           print()
        else:
            t.extend(dict[k])
    t = set(t)
    print(t)
    print(len(t))
    return dict,t

from datasketch import MinHash,MinHashLSHForest
def getMinHashs(data):
    minhashs = []
    for item in data:
        m = MinHash(num_perm=128)
        s = set(item.split(" "))
        for d in s:
            m.update(d.encode('utf8'))
        minhashs.append(m)
    return minhashs

def getMinhashforest(data):
    # Create a MinHash LSH Forest with the same num_perm parameter
    forest = MinHashLSHForest(num_perm=128)
    minhashs = getMinHashs(data=data)
    for i in range(len(minhashs)):
        # Add m2 and m3 into the index
        forest.add(i, minhashs[i])
    # IMPORTANT: must call index() otherwise the keys won't be searchable
    forest.index()
    return forest

def getMinhashforest2(minhashs):
    # Create a MinHash LSH Forest with the same num_perm parameter
    forest = MinHashLSHForest(num_perm=128)
    for i in range(len(minhashs)):
        # Add m2 and m3 into the index
        forest.add(i, minhashs[i])
    # IMPORTANT: must call index() otherwise the keys won't be searchable
    forest.index()
    return forest


def getAttributeProgress(userid,user):
    total = Cora_labeled.objects.all().count()
    attributeprogress = {}
    attributes = models.sigirCoraAttr.objects.filter(userid=userid)
    for attribute in attributes:
        coras = models.sigirCoraToAttrEntity.objects.filter(user=user,attrsynonym__value__attr_id=attribute.id)
        coraset = set([ item.cora_id for item in coras])
        print(attribute.attrname,':',len(coraset))
        # attributeprogress[attribute.attrname] = 100*len(coraset)/total
        # attributeprogress[attribute.attrname] = 100 * round(len(coraset) / total, 4)
        a = format(100*float(len(coraset)) / float(total), '.2f')
        if len(a) == 4:
            a = '0'+a
        attributeprogress[attribute.attrname] = a
    return  attributeprogress