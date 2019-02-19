from django.shortcuts import render
from sigirexperiments import performancemeasure
from ERtasks.models import Cora_labeled,Cora
from sigirexperiments import  models
from register.models import WorkLog, WorkerInfo
from  pyweb import  dxaconstants
import json
import dedupe
import os
from django.http import HttpResponse
from baselinealloy.castgather import searchmh,findtail
from baselinealloy import  headcast
from baselinealloy import models as alloymodels
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sigirexperiments import recordsampling,featuresampling,clustering,processhelper,dextrapreclustering,patternRecommendation,hbf,trainingGenerator
from django.db.models import Q

training_file = 'cora_records_randsampling80_training.json'
settings_file = 'cora_records_randsampling80_learned_settings'

workeroperatiionNum = 10
#samplemth = dxaconstants.RecordSamplingMethod.UncertainSampling
#samplemth = dxaconstants.RecordSamplingMethod.SearchSampling
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingIG
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingIGPattern
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingBasic
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRADIDSamplingBasic
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRADIDSamplingIGPattern
# samplemth = dxaconstants.RecordSamplingMethod.DEXTRADIDIGPatternHBFsimple4
# samplemth = dxaconstants.RecordSamplingMethod.hbfaffinegapOnlyclusterSimple
# samplemth = dxaconstants.RecordSamplingMethod.hbfClusterViewSimpleMinhash
# samplemth = dxaconstants.RecordSamplingMethod.hbfClusterViewSimpleMinhashaffinegap
samplemth = dxaconstants.RecordSamplingMethod.hbfClusterViewComplexMinhashaffinegap
# samplemth = 'attributeClassifiers'
taskc = dxaconstants.ERTASK.Cora
attrExplorationDisplayNum = 3
pattern_siblingDisplayNum = 3
content_DisplayNum = 10
attrBufferPoolSize = 15
recordBufferPoolSize = 200
expriment_result_path = 'expriment_result.json'
otherInfo = 'hbf'
clustering_result_path = 'expriment_clsuterresult.json'

DID_flag = False
# if samplemth == dxaconstants.RecordSamplingMethod.DEXTRADIDSamplingBasic:
#     DID_flag = True
dataset = Cora_labeled.objects.order_by('?')
if taskc == dxaconstants.ERTASK.Cora:
    if samplemth == dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingIG or samplemth == dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingIGPattern or samplemth == dxaconstants.RecordSamplingMethod.DEXTRARandomSamplingBasic:
        dataset = Cora_labeled.objects.order_by('?')
    elif DID_flag:
        coradataset = Cora_labeled.objects.order_by('?') #init
        clustdict = dextrapreclustering.minhashPreClustering(coradataset)
        BPid = processhelper.fulfillRecordBufferPool(clustdict=clustdict,BP_size=recordBufferPoolSize)
        # BP = [coradataset.get(id=item)  for item in BPid]
        # dataset = recordsampling.DIDsamplingInit(dataset=coradataset,BF=BP,beta=1,clustdict=clustdict)
        # dataset = dataset.order_by('orderscore').reverse()
        # dataset = recordsampling.DIDsamplingLittleInit(dataset=coradataset,beta=1,clustdict=clustdict)
        dataset = coradataset





def exploreperformance(request):

    # nmi = record_uncertainsampling_temp(request)
    # return  render(request,'sigir/exploreperformance.html',{'RecordSamplingMethod':dxaconstants.RecordSamplingMethod.UncertainSampling,'workerOperationNum':workeroperatiionNum,'data':nmi})
    # dict = record_uncertainsampling_multimeasure(request,workeroperatiionNum)
    #     # aa(request)

    # #record_common_cluster_vs_opnum(username=username)
    # record_common_cluster_measure(username=username)
    # headcast.test('1,p,a',2,9)
    # headcast.searchtfidf(seedid=885,kw='sympos,1993,tolerant',num=9)
    username = request.session['username']
    #recordsampling.DIDsampling()
    # featuresampling.IG()
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    # outputpath = 'E:\experiment_temp\dextra_randomsampling_IG_Pattern\_trainingdata\DEXTRARandomSamplingIGPattern_op10_data.json'
    # clustering.dextra_attrbute_hcluster(samplingMethod=samplemth,workeropNum=10,outputpath=outputpath,userid=data[0],username=username)
    # performancemeasure.record_common_cluster_measure(samplemth=samplemth, list=[10])
    # currentattr = models.sigirSynonymsSeedTemp.objects.filter(user=username)[0].cattr
    # dict = patternRecommendation.synonymsForCurrentAttr(data=dataset,currentAttr=currentattr)
    # for k, v in dict.items():
    #     print(k, v)
    # print(data[0])



    ahbf = hbf.constructHBFfordataset(data[0])
    print(json.dumps(ahbf))
    hbf.printHBF(ahbf)
    store_hbf_path = '_'.join([taskc.name,samplemth.name,str(workeroperatiionNum),otherInfo,'op.json'])
    fw = open(store_hbf_path, 'w', encoding='utf-8')
    json.dump(ahbf, fw, ensure_ascii=False, indent=4)
    orderhbf = hbf.constructOrderedHBF(ahbf=ahbf,dataset=dataset)
    orderhbf = hbf.computeEdges(orderhbf)
    ordered_layers_dict = orderhbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    # hbf.printOrderedHBF(orderhbf)
    # hbf.printOrderedHBFByOrder(orderhbf)
    hbf.printOrderedHBFByOrderOnly(orderhbf)
    sum_dict = hbf.estimateN_ACR(orderhbf)
    attris = models.sigirCoraAttr.objects.filter(userid=data[0])
    values = models.sigirCoraAttrValue.objects.filter(attr_id__in=[ attr.id for attr in attris])
    syns = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ value.id for value in values])
    experimentmsg = {'workerName':username,'worderid':data[0],'task':taskc.name,'method':samplemth.name,'opNum':workeroperatiionNum,'hbfstoredPath':store_hbf_path,'acr_measure':sum_dict,'U_size':attris.count(),'V_size':values.count(),'D_size':syns.count()}
    f = open(expriment_result_path,'a')
    json.dump(experimentmsg, f, ensure_ascii=False, indent=4)
    f.write('\n')
    f.close()
    print(json.dumps(experimentmsg))
    cluster_dict = hbf.hbfClusterViewComplexMinhashaffinegap(corahbf=orderhbf,dataset=dataset,acr_threshold=0.3,username=username,dis_threshold=3)
    for k,v in cluster_dict.items():
        models.CoraPerformanceLog.objects.create(
            explorationMethod=samplemth, clusterid=v,
            cora_id=k, confidence=-1, workerOperationNum=workeroperatiionNum)
    clusterresultdict = performancemeasure.record_sampling_clustermultimeasure_vs_opnum(wn=workeroperatiionNum,samplemth=samplemth)
    ff = open(clustering_result_path, 'a')
    json.dump(clusterresultdict, ff, ensure_ascii=False, indent=4)
    ff.write('\n')
    ff.close()


    # traingdata_path = '_'.join(['training',taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.train'])
    # testingdata_path = '_'.join(['testing', taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.test'])
    # validationdata_path = '_'.join(['validation', taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.dev'])
    # traingdata, testingdata, validationdata = trainingGenerator.basicTrainingDataDenseGenerator(username=username)
    # processhelper.writeTraingTest(traingdata_path,traingdata)
    # processhelper.writeTraingTest(testingdata_path,testingdata)
    # processhelper.writeTraingTest(validationdata_path, validationdata)

    # recommendation_from_classifiers = processhelper.preocessPredictedResult(r'C:\Users\sayarara\Desktop\experiment_classifiers\basic_dense\predicted.txt')
    # filtered_dict = processhelper.filterPredictedResult(recommendation_from_classifiers,userid=data[0])
    # for k,v in filtered_dict.items():
    #     print(k,len(v))
    #     print(v)
    # f = open('filtered_recommendation_from_basic_classifiers','a')
    # json.dump(filtered_dict, f, ensure_ascii=False, indent=4)
    # attras = models.sigirCoraAttr.objects.filter(userid=data[0])
    # for attra in attras:
    #     traingdata, testingdata, validationdata = trainingGenerator.AttributeTrainingDataGenerator(username=username,attr_id=attra.id)
    #     traingdata_path = '_'.join([attra.attrname,taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.train'])
    #     testingdata_path = '_'.join([attra.attrname, taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.test'])
    #     validationdata_path = '_'.join([attra.attrname, taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, '.dev'])
    #     processhelper.writeTraingTest(traingdata_path,traingdata)
    #     processhelper.writeTraingTest(testingdata_path,testingdata)
    #     processhelper.writeTraingTest(validationdata_path, validationdata)
    #     allennlp_test_path = '_'.join([attra.attrname, taskc.name, samplemth.name, str(workeroperatiionNum), otherInfo, 'json.test'])
    #     processhelper.writeAllenNLPTestFormat(allennlptestpath=allennlp_test_path,originalpath=testingdata_path)



    # predicted_names_list = ['predicted_author.txt', 'predicted_confshortname.txt', 'predicted_period.txt',
    #                         'predicted_press.txt', 'predicted_year.txt', 'predicted_pages.txt', 'predicted_place.txt']
    # dir = r'C:\Users\sayarara\Desktop\experiment_classifiers\attributes_clean\predict'
    # d = []
    # synos = models.sigirCoraValueSynonym.objects.filter(userid=data[0])
    # syns_list = [syn.synonym  for syn in  synos]
    # for name in predicted_names_list:
    #     path = dir + '\\' + name
    #     print(path)
    #     dict,t = processhelper.aaa(path=path)
    #     d.append(dict['NULL'])
    #     t = set(t).difference(set(syns_list))
    #     print(t)
    #     print(len(t))
    #     nn = list(set(dict['NULL']).difference(set(syns_list)))
    #     processhelper.writeTraingTest(dir + '\\' + 'filtered_related_'+name, t)
    #     processhelper.writeTraingTest(dir + '\\' + 'filtered_not_related_' + name, nn)
    # print(d)
    #
    # inter = d[0]
    # for i in range(1, len(d)):
    #     inter = set(inter).intersection(set(d[i]))
    # print(inter)
    # inter = list(set(inter).difference(set(syns_list)))
    # processhelper.writeTraingTest(dir + '\\' + 'filtered_not_related_inter', inter)
    #
    # union = d[0]
    # for i in range(1, len(d)):
    #     union = set(union).union(set(d[i]))
    # print(union)
    # union = list(set(union).difference(set(syns_list)))
    # processhelper.writeTraingTest(dir + '\\' + 'filtered_not_related_union', union)

    # aa = patternRecommendation.synsUsingWordNet('eighth')
    # print(aa)





    # processhelper.test(dataset=dataset,username=username,userid=15)
    # testa(username=username)
    # processhelper.simpleAutoMatchDection()
    #performancemeasure.record_sampling_clustermultimeasure_vs_opnum(wn=10,samplemth=samplemth)

    # processhelper.testre(str='156')
    # testb()
    # cora = Cora_labeled.objects.all()
    #     # featuresampling.minHashFastClusterIG(clusternum=100,cora=cora)
    # data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    # processhelper.sos(attrsynonym='oxford',taskc=taskc,samplemth=samplemth,user=data[0])





    dict = {}
    return render(request, 'sigir/exploreperformance.html',
                  dict)

deduper = 0
temp_d = {}



def baselinededupeinit():
    cora = Cora_labeled.objects.all()
    # c_r = {}
    # temp_d = dict((item.id, item.text) for item in cora)
    # count = 1
    for item in cora:
        # c_r['id']=item.id
        # c_r['text'] = item.text
        # clean_row = dict([('text',item.text),('id',item.id)])
        clean_row = dict([('text', item.text), ('id', str(item.id))])
        temp_d[item.id] = dict(clean_row)
    fields = [{'field': 'text', 'type': 'Text'}]
    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)
    deduper.sample(temp_d)

def testb():
    cora = Cora_labeled.objects.all()
    for item in cora:
        item.cleantext = processhelper.simpledatacleaning(item.text)
        item.save()
    print("done")


def testa(username):
    cora = Cora_labeled.objects.all()
    # c_r = {}
    # temp_d = dict((item.id, item.text) for item in cora)
    # count = 1
    for item in cora:
        # c_r['id']=item.id
        # c_r['text'] = item.text
        # clean_row = dict([('text',item.text),('id',item.id)])
        clean_row = dict([('text', item.text), ('id', str(item.id))])
        temp_d[item.id] = dict(clean_row)
    fields = [{'field': 'text', 'type': 'Text'}]
    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)
    deduper.sample(temp_d)
    clustering.testnosamplingclustering(deduper=deduper,username=username,samplingMethod=dxaconstants.RecordSamplingMethod.UncertainSampling,workeropNum=20,temp_d=temp_d)
# Create your views here.

def entityview(request):
    return render(request,'sigir/entityview.html')


def exploration(request):
    username = request.session['username']
    print(username)
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    # if DID_flag:
    #     # dataset = recordsampling.DIDsamplingInit(dataset=coradataset, BF=coradataset, beta=1,
    #     #                                          clustdict=clustdict)
    #     # dataset = recordsampling.DIDsampling(dataset=coradataset, BF=coradataset, username=username, userid=data[0],
    #     #                                      attra_id=attrid, beta=1, clustdict=clustdict)
    #     # dataset = recordsampling.DIDsamplingNoAttr(dataset=coradataset,BF=BP,username=username,userid=data[0],clustdict=clustdict)
    #     dataset = recordsampling.DIDsamplingNoAttrLittle(dataset=coradataset,BF=BPid,username=username,userid=data[0],clustdict=clustdict,beta=1)
    #     dataset = dataset.order_by('orderscore').reverse()
    # if request.method == 'POST':
    #     attribute_editor = request.POST.get("attribute_editor")
    #     attrbute_create = request.POST.get("attribute_create")
    #     print(attrbute_create)
    #     multis = request.POST.getlist("IG")
    #     print(multis)
    #     submittype = request.POST.get("submit")
    #     print(submittype)
    #     if submittype == "create and bind":
    #         # pseedid = request.POST.get("pseedid")
    #         print("create and bind")
    # list_sort_value_desc = featuresampling.IG()

    if request.is_ajax():
        print(request.body)
        print(request.POST)
        searchkey = request.POST.get('searchkey')
        page = request.POST.get('page')
        print(searchkey)
        # cora_list = Cora_labeled.objects.filter(text__contains=searchkey)
        cora_list = dataset.filter(text__contains=searchkey)
        print(cora_list)
        paginator = Paginator(cora_list, content_DisplayNum)
        try:
            cora = paginator.page(page)
        except PageNotAnInteger:
            # first page
            cora = paginator.page(1)
        except EmptyPage:
            # last page
            cora = paginator.page(paginator.num_pages)
        response = HttpResponse();
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps({'rows': cora, 'total': len(cora)}))
        return response
    else:
        searchkey = request.GET.get('q',"")
        print(searchkey)
        if searchkey:
            # cora_list = Cora_labeled.objects.filter(text__icontains=searchkey)
            # request.session['q'] = searchkey
            cora_list = dataset.filter(text__contains=searchkey)
        else:
            # searchkey = request.session['q']
            # if searchkey:
            #     cora_list = Cora.objects.filter(text__contains=searchkey)
            # else:
            #     cora_list = Cora.objects.all
            # cora_list = Cora_labeled.objects.all()
            cora_list = dataset
        print(searchkey)
        paginator = Paginator(cora_list,content_DisplayNum) # Show 10 per page
        page = request.GET.get('page')
        print(page)
        attrpage = request.GET.get('attrpage')
        print(attrpage)
        # attrpaginator = Paginator(list_sort_value_desc, 10)
        if attrpage:
            attrpage = int(attrpage)
        else:
            attrpage = 1

        try:
            cora = paginator.page(page)
        except PageNotAnInteger:
         # first page
            cora = paginator.page(1)
        except EmptyPage:
        # last page
            cora = paginator.page(paginator.num_pages)
        # try:
        #     attrig = attrpaginator.page(attrpage)
        # except PageNotAnInteger:
        #  # first page
        #     attrig = attrpaginator.page(1)
        # except EmptyPage:
        # # last page
        #     attrig = attrpaginator.page(attrpaginator.num_pages)
        # coraa = Cora_labeled.objects.all()
        # list_sort_value_desc = featuresampling.minHashFastClusterIG(clusternum=100, cora=coraa)
        # print(list_sort_value_desc[0:10])
        # return render(request, 'sigir/exploration.html',{'data': cora,'searchkey':searchkey,'attrIG':list_sort_value_desc[0+attrExplorationDisplayNum*(attrpage-1):attrExplorationDisplayNum*attrpage]})

        if not models.sigirAttrExploration.objects.filter(user=username):
            # init the substrings with information gain
            featuresampling.minHashFastClusterIG(clusternum=100,cora=dataset,username=username)
        attrexplo = models.sigirAttrExploration.objects.filter(user=username,is_labelled=False).order_by('orderscore').reverse()
        a = [ item.substring for item in  attrexplo]
        print(a)
        matches = []
        seeds = models.patternSeedTemp.objects.filter(user=username)
        attrname = ''
        if seeds:

            seedslist = processhelper.str2list(seedstr=seeds[0].seedsubstring, deli='###')
            print(seedslist)
            syn = models.sigirCoraValueSynonym.objects.filter(synonym=seedslist[0],userid=data[0])[0]
            attrname = syn.value.attr.attrname
            attrid = syn.value.attr_id
            # if DID_flag:
            #     # dataset = recordsampling.DIDsamplingInit(dataset=coradataset, BF=coradataset, beta=1,
            #     #                                          clustdict=clustdict)
            #     # dataset = recordsampling.DIDsampling(dataset=coradataset,BF=BP,username=username,userid=data[0],attra_id=attrid,beta=1,clustdict=clustdict)
            #     dataset = recordsampling.DIDsamplingLittle(dataset=coradataset,BF=BPid,username=username,userid=data[0],attra_id=attrid,beta=1,clustdict=clustdict)
            #     dataset = dataset.order_by('orderscore').reverse()
            values = models.sigirCoraAttrValue.objects.filter(attr_id=attrid, userid=data[0])
            osysn = models.sigirCoraValueSynonym.objects.filter(value_id__in=[item.id for item in values])
            match = patternRecommendation.findCandidateSilbings(seedslist=seedslist, data=dataset)
            matches = list(set(match).difference(set([item.synonym for item in osysn])))[0:pattern_siblingDisplayNum]

        stadvalname = ''
        valsyns = []
        curentattrias  = models.sigirSynonymsSeedTemp.objects.filter(user=username)
        if curentattrias:
            currentattr = curentattrias[0].cattr
            dict = patternRecommendation.synonymsForCurrentAttr(data=dataset, currentAttr=currentattr)
            if len(dict) == 0:
                stadvalname = ''
                valsyns = []
            else:
                a = sorted(dict.items())[0]
                stadvalname =a[0]
                valsyns = a[1]
        entityprogress = '08.33'
        # attributeprogress = {'year':60,'pages':50,'period':80}
        attributeprogress = processhelper.getAttributeProgress(userid=data[0],user=username)
        print(attributeprogress)
        return render(request, 'sigir/exploration.html', {'epg':entityprogress,'ap':attributeprogress,'ap2':attributeprogress,'data': cora, 'searchkey': searchkey,'matches':matches,'attrname':attrname,'syns':valsyns,'standvalue':stadvalname,
                                                          'attrIG2': attrexplo[
                                                                    0 + attrExplorationDisplayNum * (
                                                                                attrpage - 1):attrExplorationDisplayNum * attrpage]})

        # return render(request, 'sigir/exploration.html',
        #           {'data': cora, 'searchkey': searchkey, 'attrIG': attrig})


def attrexploration(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    print(data[0])
    if request.method == 'POST':
        attrbute_create = request.POST.get('attrname')
        print(attrbute_create)
        multis = request.POST.getlist("IG")
        print(multis)
        msg = {"attrname":attrbute_create,'selectedvalues':multis}
        models.dextraitems.objects.create(task=taskc,msg=json.dumps(msg),optype=dxaconstants.WorkerOperation.createAndBind,user=data[0],samplingMethod=samplemth)
        coraattr = models.sigirCoraAttr.objects.filter(attrname=attrbute_create,userid=data[0])





        if not coraattr:
            coraattr = models.sigirCoraAttr(attrname=attrbute_create, attrscope='local', is_alive=1, userid=data[0])
            coraattr.save()
        else:
            coraattr = coraattr[0]
        print(coraattr.id,coraattr.attrname)
        values = models.sigirAttrExploration.objects.filter(id__in = multis)
        seeds = [ item.substring for item in  values]
        ss = models.patternSeedTemp.objects.filter(user=username)
        seedsstr = processhelper.list2str(seedslist=seeds,deli='###')
        if ss:
            ss[0].seedsubstring = seedsstr
            ss[0].save()
            models.sigirSynonymsSeedTemp.objects.filter(user=username).update(cattr=coraattr)
        else:
            models.patternSeedTemp.objects.create(seedsubstring=seedsstr,user=username)
            models.sigirSynonymsSeedTemp.objects.create(cattr=coraattr,user=username)
        substrings = models.sigirAttrExploration.objects.filter(is_labelled=False,user=username).order_by('orderscore').reverse()[
                     0:attrBufferPoolSize]
        #decay
        for item in  substrings:
            if item.id not in multis:
                item.orderscore = item.orderscore*0.8
                item.save()
        for item in values:
            print(item.substring)
            val = models.sigirCoraAttrValue(attr_id=coraattr.id, value=item.substring, userid=data[0])
            val.save()
            corasyno = models.sigirCoraValueSynonym(value=val, synonym=item.substring, userid=data[0])
            corasyno.save()
            # if len(item.substring) < 4:
            #     # check boundaries
            #     print(item.substring)
            #     llist = Cora_labeled.objects.filter(cleantext__icontains=' '+item.substring+' ')
            # else:
            #     llist = Cora_labeled.objects.filter(text__icontains=item.substring)
            # llist = Cora_labeled.objects.filter(Q(cleantext__icontains=' ' + item.substring + ' ')| Q(cleantext__istartswith=item.substring + ' ')| Q(cleantext__iendswith=' ' + item.substring))
            # llist = dataset.filter(
            #     Q(cleantext__icontains=' ' + item.substring + ' ') | Q(cleantext__istartswith=item.substring + ' ') | Q(
            #         cleantext__iendswith=' ' + item.substring))
            #
            #
            # # restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
            # restr = '<span class = "detailtext">' + item.substring + '<span class="deli">|</span><span class="summaryText">' + coraattr.attrname + '.' + item.substring + '</span></span>'
            llist = processhelper.datasetfilteringMultiContitiion(dataset=dataset, substring=item.substring)
            restr = processhelper.viewhelper(substring=item.substring, attrbute_name=coraattr.attrname, value=item.substring)
            for entiy in llist:
                entiy.labeledtext = entiy.labeledtext.replace(item.substring, restr)
                entiy.save()
                models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno,user=username)
            # item.delete()
            item.is_labelled = True
            item.save()
    # substrings = models.sigirAttrExploration.objects.all()[0:attrBufferPoolSize]
    substrings = models.sigirAttrExploration.objects.filter(is_labelled=False,user=username).order_by('orderscore').reverse()[0:attrBufferPoolSize]
    return render(request, 'sigir/attrexploration.html',{'attrIG':substrings})


def pattern_siblings(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    if request.method == 'POST':
        attrbute_name = request.POST.get('attrname')
        print(attrbute_name)
        attr = models.sigirCoraAttr.objects.get(attrname=attrbute_name,userid=data[0])
        multis = request.POST.getlist("_selected_siblings")
        print(multis)
        # a = [ str(item) for item in multis]
        # print(a)
        seedsstr = processhelper.list2str(seedslist=multis, deli='###')
        seedtemp = models.patternSeedTemp.objects.get(user=username)
        seedtemp.seedsubstring = seedsstr
        seedtemp.save()
        for substring in multis:
            val = models.sigirCoraAttrValue(attr_id=attr.id, value=substring.replace(' ','_'), userid=data[0])
            val.save()
            corasyno = models.sigirCoraValueSynonym(value=val, synonym=substring, userid=data[0])
            corasyno.save()
            llist = processhelper.datasetfilteringMultiContitiion(dataset=dataset,substring=substring)
            restr = processhelper.viewhelper(substring=substring,attrbute_name=attrbute_name,value=val.value)
            for entiy in llist:
                entiy.labeledtext = entiy.labeledtext.replace(substring, restr)
                entiy.save()
                models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno, user=username)
        models.sigirAttrExploration.objects.filter(substring__in=multis,user=username).update(is_labelled=True)
        msg = {"attrname": attrbute_name, 'selectedvalues': multis}
        models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                          optype=dxaconstants.WorkerOperation.valueBind, user=data[0],
                                          samplingMethod=samplemth)

    matches = []
    seeds = models.patternSeedTemp.objects.filter(user=username)

    if seeds:
        seedslist = processhelper.str2list(seedstr=seeds[0].seedsubstring,deli='###')
        syn = models.sigirCoraValueSynonym.objects.filter(synonym=seedslist[0],userid=data[0])[0]
        attrname = syn.value.attr.attrname
        attrid = syn.value.attr_id
        values = models.sigirCoraAttrValue.objects.filter(attr_id=attrid,userid=data[0])
        osysn = models.sigirCoraValueSynonym.objects.filter(value_id__in=[ item.id for item in values])
        match = patternRecommendation.findCandidateSilbings(seedslist=seedslist,data=dataset)
        matches = list(set(match).difference(set([item.synonym for item in osysn])))
    return render(request, 'sigir/pattern_siblings.html',{'matches':matches,'attrname':attrname})

def pattern_synonyms(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    if request.method == 'POST':
        pp = request.POST
        print(pp)
        keys = request.POST.get('kkeys')
        print(keys)
        msg = []
        if not keys:
            print("keys none")
        else:
            print(keys)
            keylist = processhelper.str2list(seedstr=keys,deli='###')
            print(keylist)

            for k in  keylist:
                multis = request.POST.getlist(k)
                print(k,'------>',multis)
                val = models.sigirCoraAttrValue.objects.filter(value=k,userid=data[0])[0]
                for item in  multis:
                    a = processhelper.updateUVDcontent(dataset=dataset,attra=val.attr,valueid=val.id,attrsynonym=item,userid=data[0],username=username)
                    msg.append(a)
        models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                          optype=dxaconstants.WorkerOperation.valueBind, user=data[0],
                                          samplingMethod=samplemth)

    dict = {}
    seeds = models.sigirSynonymsSeedTemp.objects.filter(user=username)
    if seeds:
        currentAttr = seeds[0].cattr
        dict = patternRecommendation.synonymsForCurrentAttr(data=dataset, currentAttr=currentAttr)
        keyss = '###'.join([k for k,v in dict.items()])
    return render(request, 'sigir/pattern_synonyms.html',{'dict':dict,'kkeys':keyss})





def add(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    print(data[0])
    if request.method == 'POST':
        attrname = request.POST.get('attrname')
        scope = request.POST.get('is_local')
        print(attrname, scope)
        # models.sigirCoraAttr.objects.create(attrname=attrname, attrscope=scope, is_alive=1, userid=data[0])
        coraattr = models.sigirCoraAttr(attrname=attrname, attrscope=scope, is_alive=1, userid=data[0])
        coraattr.save()
        value = request.POST.get("attrvalue").strip()
        attrsynonym = request.POST.get("attrsynonym").strip()
        print(value, attrsynonym)
        if len(value) > 0:
            if len(attrsynonym) == 0:
                attrsynonym = value

            seedsstr = processhelper.list2str(seedslist=[attrsynonym], deli='###')
            processhelper.createUpdatePatternSeed(username=username, seedsstr=seedsstr, coraattr=coraattr)
            # val = models.sigirCoraAttrValue(attr_id=coraattr.id, value=value, userid=data[0])
            # val.save()
            #
            # corasyno = models.sigirCoraValueSynonym(value=val, synonym=attrsynonym, userid=data[0])
            # corasyno.save()
            #
            # # ss = models.patternSeedTemp.objects.filter(user=username)
            # #
            # # if ss:
            # #     ss[0].seedsubstring = seedsstr
            # #     ss[0].save()
            # #     # seedtemp = models.patternSeedTemp.objects.get(user=username)
            # #     # seedtemp.seedsubstring = seedsstr
            # #     # seedtemp.save()
            # #     models.sigirSynonymsSeedTemp.objects.filter(user=username).update(cattr=coraattr)
            # # else:
            # #     models.patternSeedTemp.objects.create(seedsubstring=seedsstr, user=username)
            # #     models.sigirSynonymsSeedTemp.objects.create(cattr=coraattr, user=username)
            #
            # # llist = Cora_labeled.objects.filter(
            # #     Q(cleantext__icontains=' ' + attrsynonym + ' ') | Q(cleantext__istartswith=attrsynonym + ' ') | Q(
            # #         cleantext__iendswith=' ' + attrsynonym))
            # # llist = dataset.filter(
            # #     Q(cleantext__icontains=' ' + attrsynonym + ' ') | Q(cleantext__istartswith=attrsynonym + ' ') | Q(
            # #         cleantext__iendswith=' ' + attrsynonym))
            # # if len(llist) == 0:
            # #     llist = dataset.filter(text__icontains=attrsynonym)
            # # # restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
            # # restr = '<span class = "detailtext">' + attrsynonym + '<span class="deli">|</span><span class="summaryText">' + attrname + '.' + value + '</span></span>'
            # llist = processhelper.datasetfilteringMultiContitiion(dataset=dataset, substring=attrsynonym)
            # restr = processhelper.viewhelper(substring=attrsynonym, attrbute_name=attrname, value=value)
            # for entiy in llist:
            #     entiy.labeledtext = entiy.labeledtext.replace(attrsynonym, restr)
            #     entiy.save()
            #     models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno,user=username)
            # item = models.sigirAttrExploration.objects.filter(substring=value,user=username)
            # if item:
            #     item[0].is_labelled = True
            #     item[0].save()
            # msg = {"attrname": attrname, "value": value, "synonym": attrsynonym}
            # msg = processhelper.updateUVDcontent(dataset=dataset,attra=coraattr,value=value,attrsynonym=attrsynonym,userid=data[0],username=username)
            value = value.replace(' ','_')
            val = models.sigirCoraAttrValue(attr_id=coraattr.id, value=value, userid=data[0])
            val.save()
            msg = processhelper.updateUVDcontent(dataset=dataset, attra=coraattr, valueid=val.id, attrsynonym=attrsynonym,
                                                 userid=data[0], username=username)

            models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                              optype=dxaconstants.WorkerOperation.createAndBind, user=data[0],
                                              samplingMethod=samplemth)
        else:
            msg = {"attrname": attrname}
            WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                                   operate_flag=dxaconstants.WorkerOperation.attributeCreate, operate_user=data[0])
            models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                              optype=dxaconstants.WorkerOperation.attributeCreate, user=data[0],
                                              samplingMethod=samplemth)
    return render(request, 'sigir/add.html')


def addvalue(request):
    username = request.session['username']
    uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    if request.method == 'POST':
        print(uids[0])
        seleattr = request.POST.get("seleattr")
        print("seleattr")
        print(seleattr)
        value = request.POST.get("attrvalue").strip()
        attrsynonym = request.POST.get("attrsynonym").strip()
        print(value,attrsynonym)
        attra = models.sigirCoraAttr.objects.get(id=seleattr)

        # models.CoraAttrValue.objects.create(attr_id=seleattr,value=value,userid=uids[0])
        # val = models.sigirCoraAttrValue(attr_id=seleattr,value=value,userid=uids[0])
        # val.save()
        # # values = models.CoraAttrValue.objects.filter(value=value)
        # # print(values[0].id)
        # # models.CoraValueSynonym.objects.create(value=values[0],synonym=attrsynonym,userid=uids[0])
        # corasyno = models.sigirCoraValueSynonym(value=val,synonym=attrsynonym,userid=uids[0])
        # corasyno.save()
        # seedsstr = processhelper.list2str(seedslist=[attrsynonym], deli='###')
        # seedtemp = models.patternSeedTemp.objects.get(user=username)
        # seedtemp.seedsubstring = seedsstr
        # seedtemp.save()

        seedsstr = processhelper.list2str(seedslist=[attrsynonym], deli='###')
        processhelper.createUpdatePatternSeed(username=username,seedsstr=seedsstr,coraattr=attra)
        msg = {"attr_id":seleattr,"value":value,"synonym":attrsynonym}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora,operate_message=json.dumps(msg), operate_flag=dxaconstants.WorkerOperation.valueBind,operate_user=uids[0])
       #  llist = dataset.filter(Q(cleantext__icontains=' ' + attrsynonym + ' ')| Q(cleantext__istartswith=attrsynonym + ' ')|Q(cleantext__iendswith=' ' + attrsynonym ))
       #  if len(llist)==0:
       #      llist = dataset.filter(text__icontains=attrsynonym)
       #  attra = models.sigirCoraAttr.objects.get(id=seleattr)
       # #restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
       #  restr = '<span class = "detailtext">'+ attrsynonym +'<span class="deli">|</span><span class="summaryText">' + attra.attrname+'.'+value + '</span></span>'

        # llist = processhelper.datasetfilteringMultiContitiion(dataset=dataset, substring=attrsynonym)
        # restr = processhelper.viewhelper(substring=attrsynonym, attrbute_name=attra.attrname, value=value)
        # for entiy in llist:
        #     entiy.labeledtext = entiy.labeledtext.replace(attrsynonym,restr)
        #     entiy.save()
        #     models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id,attrsynonym=corasyno)
        # item = models.sigirAttrExploration.objects.filter(substring=attrsynonym,user=username)
        # if item:
        #     item[0].is_labelled = True
        #     item[0].save()
        # msg = {"attrname": attra.attrname, "value": value, "synonym": attrsynonym}
        value = value.replace(' ','_')
        val = models.sigirCoraAttrValue(attr_id=attra.id, value=value, userid=uids[0])
        val.save()
        msg = processhelper.updateUVDcontent(dataset=dataset,attra=attra,valueid=val.id,attrsynonym=attrsynonym,userid=uids[0],username=username)
        models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                          optype=dxaconstants.WorkerOperation.valueBind, user=uids[0],
                                          samplingMethod=samplemth)
    data = models.sigirCoraAttr.objects.filter(userid=uids[0])
    return render(request, 'sigir/addvalue.html', {'data': data})


def addsynonym(request):
    username = request.session['username']
    uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    if request.is_ajax():
        print(request.body)
        print(request.POST)
        # attrs = json.loads(request.body.decode("utf8"))
        # print(attrs)
        # attr = attrs.get("attribute")
        # print(attr)
        attribute = request.POST.get("attribute")
        print("attriname",attribute)
        test = request.POST.get("test")
        print("test",test) #ok
        test2 = request.POST.get("test2")
        print("test2",test2) #ok
        test3 = request.POST.get("test3")
        print("test3",test3)
        valuelist = models.sigirCoraAttrValue.objects.filter(attr_id=test).values('id','value')
        print(valuelist)
        htmlstr = ""

        for i in  valuelist:
            print(i['id'],i['value'])
            htmlstr = htmlstr +"<option value='"+str(i['id'])+"'>"+i['value']+"</option>"
        # a = dict(list(valuelist))
        # print(a)
        # for k,v in  a:
        #     print(k,v)
        data = {'valuestr': htmlstr}


        # data = serializers.serialize("json",valuelist)
        return HttpResponse(json.dumps(data))
        # return JsonResponse(valuelist,safe=False)

    if request.method == 'POST':
        value = request.POST.get("seleval")
        print('value:',value)
        attrsynonym = request.POST.get("attrsynonym").strip()
        print(attrsynonym)
        seleattr = request.POST.get("attrname")
        attra = models.sigirCoraAttr.objects.get(id=seleattr)
        seedsstr = processhelper.list2str(seedslist=[attrsynonym], deli='###')
        processhelper.createUpdatePatternSeed(username=username, seedsstr=seedsstr, coraattr=attra)
        # # models.CoraValueSynonym.objects.create(value_id=value, synonym=attrsynonym, userid=uids[0])
        # corasyno = models.sigirCoraValueSynonym(value_id=value, synonym=attrsynonym, userid=uids[0])
        # corasyno.save()

        msg = {"value_id": value, "synonym": attrsynonym}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.valueBind, operate_user=uids[0])
        # llist = Cora_labeled.objects.filter(labeledtext__icontains=attrsynonym)
        # llist = Cora_labeled.objects.filter(Q(cleantext__icontains=' ' + attrsynonym + ' ')| Q(cleantext__istartswith=attrsynonym + ' ')|Q(cleantext__iendswith=' ' + attrsynonym ))
        # if len(llist) == 0:
        #     llist = Cora_labeled.objects.filter(text__icontains= attrsynonym)

        # #restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
        # restr = '<span class = "detailtext">' + attrsynonym + '<span class="deli">|</span><span class="summaryText">' + attra.attrname + '.' + corasyno.value.value + '</span></span>'
        # llist = processhelper.datasetfilteringMultiContitiion(dataset=dataset, substring=attrsynonym)
        # restr = processhelper.viewhelper(substring=attrsynonym, attrbute_name=attra.attrname, value=corasyno.value.value)
        # for entiy in llist:
        #     entiy.labeledtext = entiy.labeledtext.replace(attrsynonym,restr)
        #     entiy.save()
        #     models.sigirCoraToAttrEntity.objects.create(cora_id=entiy.id, attrsynonym=corasyno)
        # item = models.sigirAttrExploration.objects.filter(substring=attrsynonym,user=username)
        # if item:
        #     item[0].is_labelled = True
        #     item[0].save()
        # msg = {"attrname": attra.attrname, "value": corasyno.value.value, "synonym": attrsynonym}
        msg = processhelper.updateUVDcontent(dataset=dataset,attra=attra,valueid=value,attrsynonym=attrsynonym,userid=uids[0],username=username)
        models.dextraitems.objects.create(task=taskc, msg=json.dumps(msg),
                                          optype=dxaconstants.WorkerOperation.valueBind, user=uids[0],
                                          samplingMethod=samplemth)
    data = models.sigirCoraAttr.objects.filter(userid=uids[0])
    return render(request, 'sigir/addsynonym.html', {'data': data})







def searchsampling(request):
    if request.method == 'POST':
        username = request.session['username']
        current = alloymodels.CoraTemp.objects.get(id=1)
        # cora = Cora.objects.get(id=current.currentCora_id)
        submittype = request.POST.get("submit")
        print(submittype)
        if submittype == "Save and check another":
            # pseedid = request.POST.get("pseedid")
            # print(pseedid)
            # cora = Cora.objects.get(id=pseedid)
            print("Save and check another")
            multis = request.POST.getlist("Records")
            print(multis)
            multitems = models.MultiItems.objects.get(seedid=current.currentCora_id,is_checked=-1)
            multitems.selectedidset = str(multis)
            multitems.is_checked = 1
            multitems.save()
            coun = models.MultiItems.objects.filter(is_checked=1,samplingMethod=samplemth).count()
            if coun > workeroperatiionNum/2:
                print(coun)
                return render(request, 'sigir/exploreperformance.html')
        elif submittype == "submitKeywords":
            # pseedid = request.POST.get("pseedid")
            # print(pseedid)
            # cora = Cora.objects.get(id=pseedid)

            print("submitKeywords")
            seed1kw = request.POST.get("seed1kw")
            print(seed1kw)
            if seed1kw:
                print(True)
                similar = headcast.searchtfidf(seedid=current.currentCora_id, kw=seed1kw, num=9)
                # similar = searchmh(kw=seed1kw, seedid=current.currentCora_id, num=9)
                print(similar)
            data = {'similar': similar, 'seed': current.currentCora}
            print(data)
            simiids = [item.id for item in similar]
            models.MultiItems.objects.create(seedid=current.currentCora_id,text1=current.currentCora.text,keywords=seed1kw, candidateidset=str(simiids),samplingMethod=samplemth,task=dxaconstants.ERTASK.Cora,user=username)
            return render(request, 'sigir/records_searchsampling.html', data)
        elif submittype == "Save":
            print("save")
        else:
            print("Replace")
        # crowdCora.objects.create(cora_id=focusedentities[fc], testsystem=dxaconstants.TestSystems.DEXTRA,
        #                          clusterid=cluid)
    fc = 0
    seed = Cora.objects.order_by('?')[:1]
    print(seed)
    print(seed[fc].id)
    current = alloymodels.CoraTemp.objects.get(id=1)
    print(current.currentCora)
    current.currentCora = seed[fc]
    current.save()
    print(current.currentCora_id)
    data = {'seed': current.currentCora}
    print("seed:")
    print(seed[fc].id)
    print(seed[fc].text)
    print("current:")
    print(current.currentCora_id)
    return render(request, 'sigir/records_searchsampling.html',data)



def record_uncertainsampling(request):

    # To train dedupe, we feed it a sample of records.
    # deduper.sample(temp_d)
    # If we have training data saved from a previous run of dedupe,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)
    username = request.session['username']
    if request.method == 'POST':
        is_same = request.POST.get('is_same')
        print(is_same)
        unpairid = request.POST.get("unpairid")
        print(unpairid)
        unpair = models.piars.objects.get(id=unpairid)
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
                               operate_system=dxaconstants.TestSystems.SigirExpriment)
        if is_same == 1:
            examples['match'].append(record_pair)
        elif is_same == 0:
            examples['distinct'].append(record_pair)
        deduper.markPairs(examples)
        match = models.piars.objects.filter(is_same=1, user=username,samplingMethod=dxaconstants.RecordSamplingMethod.UncertainSampling)
        n_match = match.count()
        print('match',n_match)
        different = models.piars.objects.filter(is_same=0, user=username, samplingMethod=dxaconstants.RecordSamplingMethod.UncertainSampling)
        n_different = different.count()
        print('different',n_different)
        if n_match + n_different < workeroperatiionNum:
            upair = deduper.uncertainPairs()

            return render(request, 'sigir/records_uncertainsampling.html',
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
                    models.CoraPerformanceLog.objects.create(explorationMethod=dxaconstants.RecordSamplingMethod.UncertainSampling,
                                               clusterid=cluster_id, cora_id=record_id,
                                               confidence=score,workerOperationNum=workeroperatiionNum)

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
                    models.CoraPerformanceLog.objects.create(explorationMethod=dxaconstants.RecordSamplingMethod.UncertainSampling, clusterid=singleton_id, cora_id=coraid,confidence=0,workerOperationNum=workeroperatiionNum)

            # a = clusterCora.objects.filter(user=username,is_checked=-1).aggregate(Min('clusterid'))
            # datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
            # print(datas)
            # sett = set(item.cora_id for item in datas)
            # coras = Cora.objects.filter(id__in=sett)
            # return render(request, 'dedupe/clusterreview.html',{'data':coras,'clusterid':a['clusterid__min']})
            cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
            print(cora_true)
            aa_true = [item.clusterid for item in cora_true]
            cluster_membership = models.CoraPerformanceLog.objects.filter(
                explorationMethod='RecordSamplingMethod.UncertainSampling',workerOperationNum=workeroperatiionNum).order_by('cora_id')
            bb_pred = [item.clusterid for item in cluster_membership]
            nmi = performancemeasure.clusterNMI(y_true=aa_true, y_pred=bb_pred)
            dict = performancemeasure.clusterMeasureSet(aa_true=aa_true, bb_pred=bb_pred,
                                                        RecordSamplingMethod=samplemth,
                                                        workerOperationNum=workeroperatiionNum)
            return render(request,'sigir/exploreperformance.html',dict)



    upair = deduper.uncertainPairs()
    print(upair)
    print(upair[0][0])
    print(upair[0][1])
    unpair = models.piars(id1=upair[0][0]['id'],id2=upair[0][1]['id'],text1=upair[0][0]['text'],
                                   text2=upair[0][1]['text'],task=dxaconstants.ERTASK.Cora,user=username,samplingMethod=dxaconstants.RecordSamplingMethod.UncertainSampling)
    unpair.save()
    n_match = models.piars.objects.filter(is_same=1, user=username, samplingMethod=samplemth).count()
    n_different = models.piars.objects.filter(is_same=0, user=username, samplingMethod=samplemth).count()
    return render(request,'sigir/records_uncertainsampling.html',{"record1": upair[0][0], "record2": upair[0][1],
                                                     'unid': unpair.id,'n_match':n_match,'n_different':n_different})
    # return render(request, 'dedupe/activelabel.html', {"upair": upair[0]})


def record_randomsampling(request):

    # To train dedupe, we feed it a sample of records.
    # deduper.sample(temp_d)
    # If we have training data saved from a previous run of dedupe,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
    # if os.path.exists(training_file):
    #     print('reading labeled examples from ', training_file)
    #     with open(training_file, 'rb') as f:
    #         deduper.readTraining(f)
    username = request.session['username']
    if request.method == 'POST':
        is_same = request.POST.get('is_same')
        print(is_same)
        unpairid = request.POST.get("unpairid")
        print(unpairid)
        unpair = models.piars.objects.get(id=unpairid)
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
                               operate_system=dxaconstants.TestSystems.SigirExpriment)
        if is_same == 1:
            examples['match'].append(record_pair)
        elif is_same == 0:
            examples['distinct'].append(record_pair)
        deduper.markPairs(examples)
        match = models.piars.objects.filter(is_same=1, user=username,samplingMethod=samplemth)
        n_match = match.count()
        print('match',n_match)
        different = models.piars.objects.filter(is_same=0, user=username, samplingMethod=samplemth)
        n_different = different.count()
        print('different',n_different)
        if n_match + n_different < workeroperatiionNum:
            randpair = Cora.objects.order_by('?')[:2]
            unpair = models.piars(id1=randpair[0].id, id2=randpair[1].id, text1=randpair[0].text,
                                  text2=randpair[1].text, task=dxaconstants.ERTASK.Cora, user=username,
                                  samplingMethod=samplemth)
            unpair.save()
            return render(request, 'sigir/records_randomsampling.html',
                          {"record1": randpair[0], "record2": randpair[1],
                           'unid': unpair.id, 'n_match': n_match, 'n_different': n_different})
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

            # print(deduper.blocker.index_fields)
            #
            # for field in deduper.blocker.index_fields:
            #     print(field)
            #     # field_data = set(record[field] for record in temp_d)
            #     # print(temp_d)
            #     # for record in temp_d:
            #     #     print(record)
            #     #     print(temp_d[record][field])
            #     field_data = set(temp_d[record][field] for record in temp_d)
            #     print(field_data)
            #     deduper.blocker.index(data=field_data, field=field)
            # # deduper.blocker.indexAll(temp_d)
            # block_ids = deduper.blocker(temp_d, target=False)
            # print("block_ids")
            # print(block_ids)

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
                    models.CoraPerformanceLog.objects.create(explorationMethod=samplemth,
                                               clusterid=cluster_id, cora_id=record_id,
                                               confidence=score,workerOperationNum=workeroperatiionNum)

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
                    models.CoraPerformanceLog.objects.create(explorationMethod=samplemth, clusterid=singleton_id, cora_id=coraid,confidence=0,workerOperationNum=workeroperatiionNum)

            # a = clusterCora.objects.filter(user=username,is_checked=-1).aggregate(Min('clusterid'))
            # datas = clusterCora.objects.filter(clusterid=a['clusterid__min'])
            # print(datas)
            # sett = set(item.cora_id for item in datas)
            # coras = Cora.objects.filter(id__in=sett)
            # return render(request, 'dedupe/clusterreview.html',{'data':coras,'clusterid':a['clusterid__min']})
            cora_true = models.CoraPerformanceLog.objects.filter(explorationMethod='groundtruth').order_by('cora_id')
            print(cora_true)
            aa_true = [item.clusterid for item in cora_true]
            cluster_membership = models.CoraPerformanceLog.objects.filter(
                explorationMethod=samplemth,workerOperationNum=workeroperatiionNum).order_by('cora_id')
            bb_pred = [item.clusterid for item in cluster_membership]
            nmi = performancemeasure.clusterNMI(y_true=aa_true, y_pred=bb_pred)
            dict = performancemeasure.clusterMeasureSet(aa_true=aa_true,bb_pred=bb_pred,RecordSamplingMethod=samplemth,workerOperationNum=workeroperatiionNum)
            return render(request,'sigir/exploreperformance.html',dict)

    randpair = Cora.objects.order_by('?')[:2]
    print(randpair)
    for item in  randpair:
        print(item)
        print(item.id)


    print(randpair[0].id)
    print(randpair[1].id)
    upair = deduper.uncertainPairs()
    # print(upair)
    #     # print(upair[0][0])
    #     # print(upair[0][1])
    unpair = models.piars(id1=randpair[0].id,id2=randpair[1].id,text1=randpair[0].text,
                                   text2=randpair[1].text,task=dxaconstants.ERTASK.Cora,user=username,samplingMethod=samplemth)
    unpair.save()
    n_match = models.piars.objects.filter(is_same=1, user=username,samplingMethod=samplemth).count()
    n_different = models.piars.objects.filter(is_same=0, user=username,samplingMethod=samplemth).count()
    return render(request,'sigir/records_uncertainsampling.html',{"record1": randpair[0], "record2": randpair[1],
                                                     'unid': unpair.id,'n_match':n_match,'n_different':n_different})

    # return render(request, 'dedupe/activelabel.html', {"upair": upair[0]})