from DEXTRA import precluster
from  ERtasks.models import Cora_labeled
from sigirexperiments import models,dextrapreclustering
from datasketch import MinHash

def DIDsamplingtest():
    groups = precluster.preclusterTest()
    print(groups)
    return 0


def DIDsampling(dataset,BF,username,userid,attra_id,beta,clustdict):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])
    record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym__value__attr_id=attra_id)
    record_noAttra = dataset.exclude(id__in = [ item.cora_id for item in record_hasAttra])




    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    sum = 0.000001
    for record in BF:
        sum = sum + len(clustdict[cluster_membership[record.id]])
    for record in BF:
        # AC
        cora2ae = models.sigirCoraToAttrEntity.objects.filter(cora_id=record.id,user=username)
        if cora2ae:
            list = [ item.attrsynonym.value.attr.id for item in cora2ae]
            if attra_id in list:
                record.orderscore = 0
                record.save()
                continue
            else:
                ac = 1-len(list)/models.sigirCoraAttr.objects.filter(userid=userid).count()
        else:
            ac = 1

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/record_noAttra.count()
        record_minhash = MinHash(num_perm=128)
        s = set(record.cleantext.split(" "))
        for d in s:
            record_minhash.update(d.encode('utf8'))
        term2sum = 0
        for rr in BF:
            rr_minhash =  MinHash(num_perm=128)
            ss = set(rr.cleantext.split(" "))
            for dd in ss:
                rr_minhash.update(dd.encode('utf8'))
            sim = record_minhash.jaccard(rr_minhash)
            sim = (sim/sum)**beta
            term2sum = term2sum + sim
        did = ac*ic*term2sum
        record.orderscore = did
        record.save()
    return BF

def DIDsamplingNoAttr(dataset,BF,username,userid,beta,clustdict):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])



    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    sum = 0.000001
    for record in BF:
        sum = sum + len(clustdict[cluster_membership[record.id]])
    for record in BF:
        # AC
        cora2ae = models.sigirCoraToAttrEntity.objects.filter(cora_id=record.id,user=username)
        if cora2ae:
            list = [item.attrsynonym.value.attr.id for item in cora2ae]
            ac = 1 - len(list) / models.sigirCoraAttr.objects.filter(userid=userid).count()
        else:
            ac = 1

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/dataset.count()
        record_minhash = MinHash(num_perm=128)
        s = set(record.cleantext.split(" "))
        for d in s:
            record_minhash.update(d.encode('utf8'))
        term2sum = 0
        for rr in BF:
            rr_minhash =  MinHash(num_perm=128)
            ss = set(rr.cleantext.split(" "))
            for dd in ss:
                rr_minhash.update(dd.encode('utf8'))
            sim = record_minhash.jaccard(rr_minhash)
            sim = (sim/sum)**beta
            term2sum = term2sum + sim
        did = ac*ic*term2sum
        record.orderscore = did
        record.save()
    return BF


def DIDsamplingInit(dataset,BF,clustdict,beta):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])



    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k
    sum = 0.000001
    for record in BF:
        sum = sum + len(clustdict[cluster_membership[record.id]])
    for record in BF:

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/dataset.count()
        record_minhash = MinHash(num_perm=128)
        s = set(record.cleantext.split(" "))
        for d in s:
            record_minhash.update(d.encode('utf8'))
        term2sum = 0
        for rr in BF:
            rr_minhash =  MinHash(num_perm=128)
            ss = set(rr.cleantext.split(" "))
            for dd in ss:
                rr_minhash.update(dd.encode('utf8'))
            sim = record_minhash.jaccard(rr_minhash)
            sim = (sim/sum)**beta
            term2sum = term2sum + sim
        did = ic*term2sum
        record.orderscore = did
        record.save()
    return BF

def DIDsamplingLittle(dataset,BF,username,userid,attra_id,beta,clustdict):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])
    record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym__value__attr_id=attra_id)
    record_noAttra = dataset.exclude(id__in = [ item.cora_id for item in record_hasAttra])




    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    sum = dataset.count()
    for record in dataset:
        # AC
        cora2ae = models.sigirCoraToAttrEntity.objects.filter(cora_id=record.id,user=username)
        if cora2ae:
            list = [ item.attrsynonym.value.attr.id for item in cora2ae]
            if attra_id in list:
                record.orderscore = 0
                record.save()
                continue
            else:
                ac = 1-len(list)/models.sigirCoraAttr.objects.filter(userid=userid).count()
        else:
            ac = 1

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/record_noAttra.count()
        record_minhash = MinHash(num_perm=128)
        s = set(record.cleantext.split(" "))
        for d in s:
            record_minhash.update(d.encode('utf8'))
        term2sum = 0
        for rr in BF:
            rr_minhash =  MinHash(num_perm=128)
            ss = set(dataset.get(id = rr).cleantext.split(" "))
            for dd in ss:
                rr_minhash.update(dd.encode('utf8'))
            sim = record_minhash.jaccard(rr_minhash)
            sim = (sim/sum)**beta
            term2sum = term2sum + sim
        did = ac*ic*term2sum
        record.orderscore = did
        record.save()
    return dataset

def DIDsamplingNoAttrLittle(dataset,username,userid,beta,clustdict,BF):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])



    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    # sum = 0.000001
    # for record in BF:
    #     sum = sum + len(clustdict[cluster_membership[record.id]])
    sum = dataset.count()
    for record in dataset:
        # AC
        cora2ae = models.sigirCoraToAttrEntity.objects.filter(cora_id=record.id,user=username)
        if cora2ae:
            list = [item.attrsynonym.value.attr.id for item in cora2ae]
            ac = 1 - len(list) / models.sigirCoraAttr.objects.filter(userid=userid).count()
        else:
            ac = 1

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/dataset.count()
        record_minhash = MinHash(num_perm=128)
        s = set(record.cleantext.split(" "))
        for d in s:
            record_minhash.update(d.encode('utf8'))
        term2sum = 0
        for rr in BF:
            rr_minhash =  MinHash(num_perm=128)
            print(rr)
            ss = set(dataset.filter(id=rr)[0].cleantext.split(" "))
            for dd in ss:
                rr_minhash.update(dd.encode('utf8'))
            sim = record_minhash.jaccard(rr_minhash)
            sim = (sim/sum)**beta
            term2sum = term2sum + sim
        did = ac*ic*term2sum
        record.orderscore = did
        record.save()
    return dataset


def DIDsamplingLittleInit(dataset,clustdict,beta):
    # dataset = Cora_labeled.objects.all()
    # clustdict = dextrapreclustering.minhashPreClustering(dataset)
    cluster_membership = {}
    for k, v in clustdict.items():
        for d in v:
            cluster_membership[d] = k

    # values = models.sigirCoraAttrValue.objects.filter(attr_id=attra_id)
    # attrasynonyms = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    # record_hasAttra = models.sigirCoraToAttrEntity.objects.filter(user=username,attrsynonym_id__in=[ syn.id for syn in attrasynonyms])
    sum = dataset.count
    for record in dataset:

        # distribution on dataset
        k = cluster_membership[record.id]
        ic = len(clustdict[k])/dataset.count()
        # record_minhash = MinHash(num_perm=128)
        # s = set(record.cleantext.split(" "))
        # for d in s:
        #     record_minhash.update(d.encode('utf8'))
        # term2sum = 0
        # for rr in BF:
        #     rr_minhash =  MinHash(num_perm=128)
        #     ss = set(rr.cleantext.split(" "))
        #     for dd in ss:
        #         rr_minhash.update(dd.encode('utf8'))
        #     sim = record_minhash.jaccard(rr_minhash)
        #     sim = (sim/sum)**beta
        #     term2sum = term2sum + sim
        did = ic
        record.orderscore = did
        record.save()
    return dataset