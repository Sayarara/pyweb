from sigirexperiments import  models
from sigirexperiments import  processhelper
from ERtasks.models import Cora, Cora_labeled
import dedupe
from future.utils import viewvalues

# These two generators will give us the corpora setting up the Set
# distance metrics
def titlekey(data) :
    for record in viewvalues(data) :
        yield record['titlekey']

def authors(data) :
    for record in viewvalues(data) :
        yield record['author']
def texts(data) :
    for record in viewvalues(data) :
        yield record['text']

def pages(data) :
    for record in viewvalues(data) :
        yield record['pages']

def year(data) :
    for record in viewvalues(data) :
        yield record['year']
def press(data) :
    for record in viewvalues(data) :
        yield record['press']

def period(data) :
    for record in viewvalues(data) :
        yield record['period']

def confshortnames(data) :
    for record in viewvalues(data) :
        yield record['confshortname']


def dextra_attrbute_hcluster(samplingMethod,workeropNum,outputpath,userid,username):
    temp_d = {}
    cora = Cora_labeled.objects.all()
    coraattrs = models.sigirCoraAttr.objects.filter(userid=userid)
    for item in cora:
        # c_r['id']=item.id
        # c_r['text'] = item.text
        # clean_row = dict([('text',item.text),('id',item.id)])
        # print(item.text)
        clean_row = dict([('text', item.cleantext), ('id', str(item.id))])
        cora2syns = models.sigirCoraToAttrEntity.objects.filter(cora_id=item.id,user=username)
        # for syn in  cora2syns:
        #         #     print(syn.attrsynonym.value.attr.attrname)
        #         #     print(syn.attrsynonym.value.value)
        #         #     clean_row[syn.attrsynonym.value.attr.attrname] =[].append(syn.attrsynonym.value.value)
        #         # print(clean_row)
        #         # for attr in  coraattrs:
        #         #     if clean_row[attr.attrname]:
        #         #         clean_row[attr.attrname] = tuple(sorted(clean_row[attr.attrname]))
        #         #     else:
        #         #         clean_row[attr.attrname] = None

        # print(clean_row)
        for attr in  coraattrs:
            clean_row[str(attr.attrname)] = []
            # print(type(attr.attrname))
        for syn in cora2syns:
            # print(syn.attrsynonym.value.attr.attrname)
            # print(syn.attrsynonym.value.value)
            clean_row[str(syn.attrsynonym.value.attr.attrname)].append(str(syn.attrsynonym.value.value))
        #     print('-------------------')
        #     print(type(syn.attrsynonym.value.attr.attrname), type(syn.attrsynonym.value.value))
        # # print(clean_row)
        for attr in coraattrs:
            if len(clean_row[str(attr.attrname)]) == 0:
                clean_row[str(attr.attrname)] = None
            else:
                clean_row[str(attr.attrname)] = tuple(sorted(clean_row[attr.attrname]))
                # if len(clean_row[str(attr.attrname)]) == 1 and str(attr.attrname) != 'author' and str(attr.attrname) != 'titlekey':
                #     clean_row[str(attr.attrname)] = clean_row[attr.attrname][0]
                #     # print(clean_row[attr.attrname])
                # else:
                #     clean_row[str(attr.attrname)] = tuple(sorted(clean_row[attr.attrname]))
                #     if str(attr.attrname) == 'author' or str(attr.attrname) == 'titlekey'or str(attr.attrname)=='page':
                #         attr
                #     else:
                #         print(clean_row[str(attr.attrname)])

        # print(clean_row)
        temp_d[item.id] = dict(clean_row)
        # for attr in coraattrs:
    # for item in  temp_d:
    #     print(item)
    #     print(temp_d[item])

    processhelper.storeTrasingData(outputpath=outputpath,data=temp_d)
    fields1 = [
        {'field': 'year',
         'type': 'Exact',
         'has missing': True},
        {'field': 'press',
         'type': 'String',
         'has missing': True},
        {'field': 'confshortname',
         'type': 'String',
         'has missing': True},
        {'field': 'period',
         'type': 'String',
         'has missing': True},
        {'field': 'titlekey',
         'type': 'Set',
         'corpus': titlekey(temp_d),
         'has missing': True},
        {'field': 'author',
         'type': 'Set',
         'corpus': authors(temp_d),
         'has missing': True},
        {'field': 'page',
         'type': 'Set',
         'corpus': pages(temp_d),
         'has missing': True},
        {'field': 'text',
         'type': 'Text'}
    ]
    # text ok,titlekey ok,author ok, confshortname ok,period ok,year ok
    # year wrong, press wrong
    #
    # fields = [
    #     {'field': 'confshortname',
    #      'type': 'Set',
    #      'corpus': confshortnames(temp_d),
    #      'has missing': True},
    #     {'field': 'press',
    #      'type': 'Set',
    #      'corpus': press(temp_d),
    #      'has missing': True},
    #     {'field': 'year',
    #      'type': 'Set',
    #      'corpus': year(temp_d),
    #      'has missing': True},
    #     {'field': 'period',
    #      'type': 'Set',
    #      'corpus': period(temp_d),
    #      'has missing': True},
    #     {'field': 'titlekey',
    #      'type': 'Set',
    #      'corpus': titlekey(temp_d),
    #      'has missing': True},
    #     {'field': 'author',
    #      'type': 'Set',
    #      'corpus': authors(temp_d),
    #      'has missing': True},
    #     {'field': 'page',
    #      'type': 'Set',
    #      'corpus': pages(temp_d),
    #      'has missing': True},
    #     {'field': 'text',
    #      'type': 'Text'}
    # ]
    fields = [
        {'field': 'confshortname',
         'type': 'Set',
         'corpus': confshortnames(temp_d),
         'has missing': True},
        {'field': 'press',
         'type': 'Set',
         'corpus': press(temp_d),
         'has missing': True},
        {'field': 'year',
         'type': 'Set',
         'corpus': year(temp_d),
         'has missing': True},
        {'field': 'period',
         'type': 'Set',
         'corpus': period(temp_d),
         'has missing': True},
        {'field': 'pages',
         'type': 'Set',
         'corpus': pages(temp_d),
         'has missing': True},
        {'field': 'text',
         'type': 'Text'}
    ]
    # Create a new deduper object and pass our data model to it.

    deduper = dedupe.Dedupe(fields)
    deduper.sample(temp_d)
    print("sample done")
    examples = processhelper.simpleAutoMatchDection(temp_d=temp_d)
    print(examples)
    deduper.markPairs(examples)
    deduper.train()
    print('train done')
    threshold = deduper.threshold(temp_d, recall_weight=1)
    print('clustering...')
    clustered_dupes = deduper.match(temp_d, threshold)

    print('# duplicate sets', len(clustered_dupes))
    cluster_membership = {}
    cluster_id = 0
    print(clustered_dupes)

    for (cluster_id, cluster) in enumerate(clustered_dupes):
        id_set, scores = cluster
        print(id_set)
        cluster_d = [temp_d[c] for c in id_set]
        print(cluster_d)
        # canonical_rep = dedupe.canonicalize(cluster_d)
        for record_id, score in zip(id_set, scores):
            cluster_membership[record_id] = {
                "cluster id": cluster_id,
                # "canonical representation": canonical_rep,
                "confidence": score

            }
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplingMethod,
                clusterid=cluster_id, cora_id=record_id,
                confidence=score, workerOperationNum=workeropNum)

    singleton_id = cluster_id + 1
    print(cluster_membership)
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    print(cora_true)
    aa = [item.clusterid for item in cora_true]
    for item in cora_true:
        coraid = item.cora_id
        if coraid in cluster_membership:
            print(coraid)
        else:
            singleton_id += 1
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplingMethod, clusterid=singleton_id,
                cora_id=coraid, confidence=0, workerOperationNum=workeropNum)
    return 0

def testnosamplingclustering(deduper,temp_d,username,samplingMethod,workeropNum):
    tempp = models.piars.objects.filter(user=username,
                                        samplingMethod=samplingMethod)[:workeropNum]
    examples = {'distinct': [], 'match': []}
    for item in tempp:
        d1 = dict([('text', item.text1), ('id', str(item.id1))])
        d2 = dict([('text', item.text2), ('id', str(item.id2))])
        record_pair = (d1, d2)
        print(item.is_same)
        if item.is_same:
            print("match")
            examples['match'].append(record_pair)
        else:
            print("not match")
            examples['distinct'].append(record_pair)
    print(examples)
    deduper.markPairs(examples)
    deduper.train()
    print('train done')
    threshold = deduper.threshold(temp_d, recall_weight=1)
    print('clustering...')
    clustered_dupes = deduper.match(temp_d, threshold)

    print('# duplicate sets', len(clustered_dupes))
    cluster_membership = {}
    cluster_id = 0
    print(clustered_dupes)

    for (cluster_id, cluster) in enumerate(clustered_dupes):
        id_set, scores = cluster
        print(id_set)
        cluster_d = [temp_d[c] for c in id_set]
        print(cluster_d)
        # canonical_rep = dedupe.canonicalize(cluster_d)
        for record_id, score in zip(id_set, scores):
            cluster_membership[record_id] = {
                "cluster id": cluster_id,
                # "canonical representation": canonical_rep,
                "confidence": score

            }

    singleton_id = cluster_id + 1
    print(cluster_membership)
    return 0

def record_clustering_vs_opnum(username,workeropNum,samplingMethod,deduper,temp_d):
    tempp = models.piars.objects.filter(user=username,
                                        samplingMethod=samplingMethod)[:workeropNum]
    examples = {'distinct': [], 'match': []}
    for item in tempp:
        d1 = dict([('text', item.text1), ('id', str(item.id1))])
        d2 = dict([('text', item.text2), ('id', str(item.id2))])
        record_pair = (d1, d2)
        print(item.is_same)
        if item.is_same:
            print("match")
            examples['match'].append(record_pair)
        else:
            print("not match")
            examples['distinct'].append(record_pair)
    print(examples)
    deduper.markPairs(examples)
    deduper.train()
    print('train done')
    threshold = deduper.threshold(temp_d, recall_weight=1)
    print('clustering...')
    clustered_dupes = deduper.match(temp_d, threshold)

    print('# duplicate sets', len(clustered_dupes))
    cluster_membership = {}
    cluster_id = 0
    print(clustered_dupes)

    for (cluster_id, cluster) in enumerate(clustered_dupes):
        id_set, scores = cluster
        print(id_set)
        cluster_d = [temp_d[c] for c in id_set]
        print(cluster_d)
        # canonical_rep = dedupe.canonicalize(cluster_d)
        for record_id, score in zip(id_set, scores):
            cluster_membership[record_id] = {
                "cluster id": cluster_id,
                # "canonical representation": canonical_rep,
                "confidence": score

            }
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplingMethod,
                clusterid=cluster_id, cora_id=record_id,
                confidence=score, workerOperationNum=workeropNum)

    singleton_id = cluster_id + 1
    print(cluster_membership)
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    print(cora_true)
    aa = [item.clusterid for item in cora_true]
    for item in cora_true:
        coraid = item.cora_id
        if coraid in cluster_membership:
            print(coraid)
        else:
            singleton_id += 1
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplingMethod, clusterid=singleton_id,
                cora_id=coraid, confidence=0, workerOperationNum=workeropNum)
    return 0



def search_clustering_vs_opnum(username,wn,samplemth,taskc,deduper,temp_d):
    tempp = models.MultiItems.objects.filter(user=username,samplingMethod=samplemth,task=taskc,is_checked=1)[:wn]
    examples = {'distinct': [], 'match': []}
    for item in tempp:
        dseed = dict([('text', item.text1), ('id', str(item.seedid))])
        candidateset = processhelper.str2list(item.candidateidset)
        print(candidateset)
        selectedset = processhelper.str2list(item.selectedidset)
        print(selectedset)
        corasimiaritems = Cora.objects.filter(id__in=selectedset)
        for selecteditem in corasimiaritems:
            d2 = dict([('text', selecteditem.text), ('id', str(selecteditem.id))])
            record_pair = (dseed, d2)
            examples['match'].append(record_pair)
        for n in range(len(corasimiaritems)):
            for i in range(0, n):
                d1 = dict([('text', corasimiaritems[n].text), ('id', str(corasimiaritems[n].id))])
                d2 = dict([('text', corasimiaritems[i].text), ('id', str(corasimiaritems[i].id))])
                record_pair = (d1, d2)
                examples['match'].append(record_pair)
        notselected = list(set(candidateset).difference(set(selectedset)))
        coranotsimilaritems = Cora.objects.filter(id__in=notselected)
        for notseleteditem in coranotsimilaritems:
            d2 = dict([('text', notseleteditem.text), ('id', str(notseleteditem.id))])
            record_pair = (dseed, d2)
            examples['distinct'].append(record_pair)
            for selecteditem in corasimiaritems:
                d1 = dict([('text', selecteditem.text), ('id', str(selecteditem.id))])
                record_pair = (d1, d2)
                examples['distinct'].append(record_pair)
    print(examples)
    deduper.markPairs(examples)
    deduper.train()
    print('train done')
    threshold = deduper.threshold(temp_d, recall_weight=1)
    print('clustering...')
    clustered_dupes = deduper.match(temp_d, threshold)

    print('# duplicate sets', len(clustered_dupes))
    cluster_membership = {}
    cluster_id = 0
    print(clustered_dupes)

    for (cluster_id, cluster) in enumerate(clustered_dupes):
        id_set, scores = cluster
        print(id_set)
        cluster_d = [temp_d[c] for c in id_set]
        print(cluster_d)
        # canonical_rep = dedupe.canonicalize(cluster_d)
        for record_id, score in zip(id_set, scores):
            cluster_membership[record_id] = {
                "cluster id": cluster_id,
                # "canonical representation": canonical_rep,
                "confidence": score

            }
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplemth,
                clusterid=cluster_id, cora_id=record_id,
                confidence=score, workerOperationNum=wn*2)

    singleton_id = cluster_id + 1
    print(cluster_membership)
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    print(cora_true)
    for item in cora_true:
        coraid = item.cora_id
        if coraid in cluster_membership:
            print(coraid)
        else:
            singleton_id += 1
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplemth, clusterid=singleton_id,
                cora_id=coraid, confidence=0, workerOperationNum=wn*2)
    return 0


def record_common_cluster(username,wn,samplemth,deduper,temp_d):
    #username = request.session['username']
    nmi = 0
    print('username:'+username)
    print("wn:")
    print(wn)
    tempp = models.piars.objects.filter(user=username,
                                        samplingMethod=samplemth)[:wn]
    examples = {'distinct': [], 'match': []}
    for item in tempp:
        d1 = dict([('text', item.text1), ('id', str(item.id1))])
        d2 = dict([('text', item.text2), ('id', str(item.id2))])
        record_pair = (d1, d2)
        print(item.is_same)
        if item.is_same:
            print("match")
            examples['match'].append(record_pair)
        else:
            #print("not match")
            examples['distinct'].append(record_pair)
    print(examples)
    deduper.markPairs(examples)
    deduper.train()
    print('train done')
    threshold = deduper.threshold(temp_d, recall_weight=1)
    print('clustering...')
    clustered_dupes = deduper.match(temp_d, threshold)

    print('# duplicate sets', len(clustered_dupes))
    cluster_membership = {}
    cluster_id = 0
    print(clustered_dupes)

    for (cluster_id, cluster) in enumerate(clustered_dupes):
        id_set, scores = cluster
        print(id_set)
        cluster_d = [temp_d[c] for c in id_set]
        print(cluster_d)
        # canonical_rep = dedupe.canonicalize(cluster_d)
        for record_id, score in zip(id_set, scores):
            cluster_membership[record_id] = {
                "cluster id": cluster_id,
                # "canonical representation": canonical_rep,
                "confidence": score

            }
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplemth,
                clusterid=cluster_id, cora_id=record_id,
                confidence=score, workerOperationNum=wn)

    singleton_id = cluster_id + 1
    print(cluster_membership)
    cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
    print(cora_true)
    aa = [item.clusterid for item in cora_true]
    for item in cora_true:
        coraid = item.cora_id
        if coraid in cluster_membership:
            print(coraid)
        else:
            singleton_id += 1
            models.CoraPerformanceLog.objects.create(
                explorationMethod=samplemth, clusterid=singleton_id,
                cora_id=coraid, confidence=0, workerOperationNum=wn)

    # a = clusterCora.objects.filter(user=username,is_checked=-1).aggregate(Min('clusterid'))
    # datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
    # print(datas)
    # sett = set(item.cora_id for item in datas)
    # coras = Cora.objects.filter(id__in=sett)
    # return render(request, 'dedupe/clusterreview.html',{'data':coras,'clusterid':a['clusterid__min']})
    cluster_membership = models.CoraPerformanceLog.objects.filter(
        explorationMethod=samplemth, workerOperationNum=wn).order_by(
        'cora_id')
    bb_pred = [item.clusterid for item in cluster_membership]
    return bb_pred


