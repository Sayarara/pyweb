from django.shortcuts import render, redirect
from ERtasks.models import Cora,clusterCora
import dedupe
from baselinededupe import models,blocking,distancetools
from  pyweb import  dxaconstants
import os
from django.db.models import Min,Max
from register.models import WorkLog, WorkerInfo
import json

import optparse
import csv
# Create your views here.

training_file = 'example_training.json'
settings_file = 'example_learned_settings'
output_file = 'example_output.csv'

temp_d = {}
cora = Cora.objects.all()
 # c_r = {}
# temp_d = dict((item.id, item.text) for item in cora)
# count = 1
for item in cora:
    # c_r['id']=item.id
     # c_r['text'] = item.text
    # clean_row = dict([('text',item.text),('id',item.id)])
    clean_row = dict([('text', item.text), ('id', str(item.id))])
    temp_d[item.id] = dict(clean_row)
    # count = count+1
# print(temp_d)
# if os.path.exists(settings_file):
# #     print('reading from', settings_file)
# #     with open(settings_file, 'rb') as f:
# #         deduper = dedupe.StaticDedupe(f)
# else:

fields = [{'field' : 'text', 'type': 'Text'}]
# Create a new deduper object and pass our data model to it.
deduper = dedupe.Dedupe(fields)
# To train dedupe, we feed it a sample of records.
deduper.sample(temp_d)
    # If we have training data saved from a previous run of dedupe,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
# if os.path.exists(training_file):
#     print('reading labeled examples from ', training_file)
#     with open(training_file, 'rb') as f:
#         deduper.readTraining(f)

def activelabel(request):
    username = request.session['username']
    if request.method == 'POST':
        is_same = request.POST.get('is_same')
        print(is_same)
        unpairid = request.POST.get("unpairid")
        print(unpairid)
        unpair = models.uncertainpiars.objects.get(id=unpairid)
        unpair.is_same = is_same
        unpair.save()
        examples = {'distinct': [], 'match': []}
        d1 = dict([('text', unpair.text1), ('id', str(unpair.id1))])
        d2 = dict([('text', unpair.text2), ('id', str(unpair.id2))])
        record_pair = (d1,d2)
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        msg = {"unpair_id1": unpair.id1, "unpair_id2": unpair.id2, "is_same": is_same}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.pairJudge, operate_user=uids[0],
                               operate_system=dxaconstants.TestSystems.Dedupe)
        if is_same == 1:
            examples['match'].append(record_pair)
        elif is_same == 0:
            examples['distinct'].append(record_pair)
        deduper.markPairs(examples)
        match = models.uncertainpiars.objects.filter(is_same=1, user=username)
        n_match = match.count()
        print('match',n_match)
        different = models.uncertainpiars.objects.filter(is_same=0, user=username)
        n_different = different.count()
        print('different',n_different)
        if n_match < 10 or n_different < 10:
            upair = deduper.uncertainPairs()
            unpair = models.uncertainpiars(id1=upair[0][0]['id'], id2=upair[0][1]['id'], text1=upair[0][0]['text'],
                                           text2=upair[0][1]['text'], task=dxaconstants.ERTASK.Cora, user=username)
            unpair.save()
            return render(request, 'dedupe/activelabel.html',
                          {"record1": upair[0][0], "record2": upair[0][1], 'unid': unpair.id, 'n_match': n_match,
                           'n_different': n_different})
        else:
            examples = {'distinct': [], 'match': []}
            for mitem in match:
                d1 = dict([('text', mitem.text1), ('id', str(mitem.id1))])
                d2 = dict([('text', mitem.text2), ('id', str(mitem.id2))])
                record_pair = (d1, d2)
                examples['match'].append(record_pair)
            for ditem in different:
                d1 = dict([('text', ditem.text1), ('id', str(ditem.id1))])
                d2 = dict([('text', ditem.text2), ('id', str(ditem.id2))])
                record_pair = (d1, d2)
                # record_pair = dict([('text', ditem.text1), ('id', ditem.id1)]) + dict(
                #     [('text', ditem.text2), ('id', ditem.id2)])
                print(record_pair)
                examples['distinct'].append(record_pair)
            print(examples)
            deduper.markPairs(examples)
            deduper.train()
            print('train done')
            # blocking.blockingsql()

            print(deduper.blocker.index_fields)

            for field in deduper.blocker.index_fields:
                print(field)
                # field_data = set(record[field] for record in temp_d)
                # print(temp_d)
                # for record in temp_d:
                #     print(record)
                #     print(temp_d[record][field])
                field_data = set(temp_d[record][field] for record in temp_d)
                print(field_data)
                deduper.blocker.index(data=field_data, field=field)
            # deduper.blocker.indexAll(temp_d)
            block_ids = deduper.blocker(temp_d, target=False)
            print("block_ids")
            print(block_ids)

            # When finished, save our training away to disk
            with open(training_file, 'w') as tf:
                deduper.writeTraining(tf)
            # Save our weights and predicates to disk.  If the settings file
            # exists, we will skip all the training and learning next time we run
            # this file.
            with open(settings_file, 'wb') as sf:
                deduper.writeSettings(sf)
            threshold = deduper.threshold(temp_d, recall_weight=1)
            print('clustering...')
            clustered_dupes = deduper.match(temp_d, threshold)

            print('# duplicate sets', len(clustered_dupes))
            cluster_membership = {}
            cluster_id = 0
            print(clustered_dupes)

            aaa = clusterCora.objects.filter(user=username)
            if aaa:
                aaa.delete()
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
                    clusterCora.objects.create(testsystem=dxaconstants.TestSystems.Dedupe,
                                               clusterid=cluster_id, cora_id=record_id,
                                               user=username, confidence=score,is_checked=-1)

            print(cluster_membership)
            # a = clusterCora.objects.filter(user=username,is_checked=-1).aggregate(Min('clusterid'))
            # datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
            # print(datas)
            # sett = set(item.cora_id for item in datas)
            # coras = Cora.objects.filter(id__in=sett)
            # return render(request, 'dedupe/clusterreview.html',{'data':coras,'clusterid':a['clusterid__min']})
            return redirect('/dedupe/clusterreview')

    # temp_d = {}
    # cora = Cora.objects.all()
    # # c_r = {}
    # # temp_d = dict((item.id, item.text) for item in cora)
    # count = 1;
    # for item in cora:
    #     # c_r['id']=item.id
    #     # c_r['text'] = item.text
    #     clean_row = dict([('text',item.text),('id',item.id)])
    #     temp_d['id'+str(count)] = dict(clean_row)
    #     count = count+1
    # print(temp_d)
    # fields = [{'field' : 'text', 'type': 'Text'}]
    # # Create a new deduper object and pass our data model to it.
    # deduper = dedupe.Dedupe(fields)
    # deduper.sample(temp_d)
    upair = deduper.uncertainPairs()
    print(upair)
    print(upair[0][0])
    print(upair[0][1])
    unpair = models.uncertainpiars(id1=upair[0][0]['id'],id2=upair[0][1]['id'],text1=upair[0][0]['text'],
                                   text2=upair[0][1]['text'],task=dxaconstants.ERTASK.Cora,user=username)
    unpair.save()
    n_match = models.uncertainpiars.objects.filter(is_same=1, user=username).count()
    n_different = models.uncertainpiars.objects.filter(is_same=0, user=username).count()
    return render(request,'dedupe/activelabel.html',{"record1": upair[0][0], "record2": upair[0][1],
                                                     'unid': unpair.id,'n_match':n_match,'n_different':n_different})
    # return render(request, 'dedupe/activelabel.html', {"upair": upair[0]})

# cluster_membershipRound2 = {}
def clusterreview(request):
    username = request.session['username']
    if request.method == 'POST':
        print("cluster review post")
        selects = request.POST.getlist("_selected_action")

        print(selects)
        clusterid = request.POST.get("clusterid")
        # clusterCora.objects.filter(clusterid=clusterid).update(is_checked=1)

        aaa = clusterCora.objects.filter(clusterid=clusterid)
        sett = set(aitem.cora_id for aitem in aaa)
        print("sett",sett)
        noset = set(int(noitem) for noitem in selects)
        print('noset:',noset)
        iyes = list(sett.difference(noset))
        print("iyes",iyes)
        clusterCora.objects.filter(cora_id__in=noset).update(is_checked=0) # no
        clusterCora.objects.filter(cora_id__in=set(iyes)).update(is_checked=1)  # yes
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        msg = {"clusterid" : clusterid, "include" : iyes, 'exclude' : list(noset)}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.clusterReview, operate_user=uids[0],
                               operate_system=dxaconstants.TestSystems.Dedupe)

        num = clusterCora.objects.filter(user=username, is_checked=-1).count()
        print("num:",num)


        if num == 0:
            clusteridlist = clusterCora.objects.values('clusterid').distinct()
            print('clusterlist:', clusteridlist)
            examples = {'distinct': [], 'match': []}
            for clusteridd in clusteridlist:
                print(clusteridd)
                print(clusteridd['clusterid'])
                aaa = clusterCora.objects.filter(clusterid=clusteridd['clusterid'])
                # sett = set(aitem.cora_id for aitem in aaa)
                nosets = clusterCora.objects.filter(clusterid=clusteridd['clusterid'],is_checked=0) # no
                yessets = clusterCora.objects.filter(clusterid=clusteridd['clusterid'], is_checked=1)  # yes
                nocoraids = set(aitem.cora_id for aitem in nosets)
                yescoraids = set(aitem.cora_id for aitem in yessets)
                inosescora = Cora.objects.filter(id__in=nocoraids)
                iyesescora = Cora.objects.filter(id__in=yescoraids)
                for nocora in inosescora:
                    d1 = dict([('text', nocora.text), ('id', str(nocora.id))])
                    for yescora in iyesescora:
                        d2 = dict([('text', yescora.text), ('id', str(yescora.id))])
                        record_pair = (d1, d2)
                        # record_pair = dict([('text', ditem.text1), ('id', ditem.id1)]) + dict(
                        #     [('text', ditem.text2), ('id', ditem.id2)])
                        print(record_pair)
                        examples['distinct'].append(record_pair)
                for yescora1 in iyesescora:
                    d1 = dict([('text', yescora1.text), ('id', str(yescora1.id))])
                    for yescora2 in iyesescora:
                        d2 = dict([('text', yescora2.text), ('id', str(yescora2.id))])
                        if not yescora1.id == yescora2.id:
                            record_pair = (d1, d2)
                            examples['match'].append(record_pair)
            if os.path.exists(training_file):
                print('reading labeled examples from ', training_file)
                with open(training_file, 'rb') as af:
                    deduper.readTraining(af)
            deduper.markPairs(examples)
            deduper.train()
            # When finished, save our training away to disk
            with open(training_file, 'w') as tf:
                deduper.writeTraining(tf)
            # Save our weights and predicates to disk.  If the settings file
            # exists, we will skip all the training and learning next time we run
            # this file.
            with open(settings_file, 'wb') as sf:
                deduper.writeSettings(sf)
            threshold = deduper.threshold(temp_d, recall_weight=1)
            print('clustering...')
            clustered_dupes = deduper.match(temp_d, threshold)

            print('# duplicate sets', len(clustered_dupes))

            cluster_id = 0
            print(clustered_dupes)

            aaa = models.clusterTemp.objects.filter(user=username)
            if aaa:
                aaa.delete()
            models.clusterCanonicalRepresentation.objects.filter(user=username).delete()
            for (cluster_id, cluster) in enumerate(clustered_dupes):
                id_set, scores = cluster
                print(id_set)
                cluster_d = [temp_d[c] for c in id_set]
                print(cluster_d)
                canonical_rep = dedupe.canonicalize(cluster_d)
                models.clusterCanonicalRepresentation.objects.create(clusterid=cluster_id,
                                                                     canonrep=canonical_rep,
                                                                     user=username,
                                                                     task=dxaconstants.ERTASK.Cora)
                for record_id, score in zip(id_set, scores):
                    # cluster_membershipRound2[record_id] = {
                    #     "cluster id": cluster_id,
                    #     "canonical representation": canonical_rep,
                    #     "confidence": score
                    #
                    # }
                    models.clusterTemp.objects.create(task_record_id=record_id,task=dxaconstants.ERTASK.Cora,clusterid=cluster_id,confidence=score,user=username)
            # print(cluster_membershipRound2)

            aaaaa = models.clusterTemp.objects.all()
            sett = set(bitem.task_record_id for bitem in aaaaa)
            corass = Cora.objects.all()
            alls = set(bitem.id for bitem in corass)
            isingle = list(alls.difference(sett))
            for single in isingle:
                models.clusterTemp.objects.create(task_record_id=single, task=dxaconstants.ERTASK.Cora,
                                                  clusterid=-1, confidence=0.0, user=username)
            return redirect('/dedupe/addtoclusters')
        else:
            a = clusterCora.objects.filter(user=username, is_checked=-1).aggregate(Min('clusterid'))
            datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
            sett = set(citem.cora_id for citem in datas)
            coras = Cora.objects.filter(id__in=sett)
            print(coras)
            return render(request, 'dedupe/clusterreview.html', {'data': coras, 'clusterid': a['clusterid__min']})
    a = clusterCora.objects.filter(user=username, is_checked=-1).aggregate(Min('clusterid'))
    print(a)
    print(a['clusterid__min'])
    datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
    print(datas)
    sett = set(bitem.cora_id for bitem in datas)
    coras = Cora.objects.filter(id__in=sett)
    print(coras)
    return render(request, 'dedupe/clusterreview.html',{'data':coras,'clusterid':a['clusterid__min']})

def addtoclusters(request):
    username = request.session['username']
    if request.method == 'POST':
        singleid = request.POST.get("_single")
        print(singleid)
        selects = request.POST.getlist("_selected_action")
        print(selects)
        if len(selects) == 0:
            maxclusternum = models.clusterTemp.objects.aggregate(Max('clusterid'))
            cluster_id = maxclusternum['clusterid__max']+1
            models.clusterTemp.objects.filter(task_record_id=singleid).update(clusterid=cluster_id)
        else:
            cluster_id = int(selects[0])
            print(cluster_id)
            models.clusterTemp.objects.filter(task_record_id=singleid).update(clusterid=cluster_id)
            for itemm in selects:
                models.clusterTemp.objects.filter(clusterid=int(itemm)).update(clusterid=cluster_id)
    singlenum = models.clusterTemp.objects.filter(user=username, clusterid=-1).count()
    if singlenum == 0:
        return redirect('/dedupe/polishclusters')
    single = models.clusterTemp.objects.filter(user=username, clusterid=-1).aggregate(Min('task_record_id'))
    print(single['task_record_id__min'])
    singeRecord = Cora.objects.get(id=single['task_record_id__min'])
    ss = distancetools.findNearestClusters(focusedentityid=single['task_record_id__min'],num=5)
    return render(request, 'dedupe/addtoclusters.html',{'single':singeRecord,'cluster':ss})


def polishclusters(request):
    return render(request, 'dedupe/polishclusters.html')