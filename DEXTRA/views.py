from django.shortcuts import render
from DEXTRA import models
from register.models import WorkerInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ERtasks.models import Cora
from register.models import WorkLog
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
from  pyweb import  dxaconstants
from django.core import serializers
from DEXTRA.clusterrefine import findSimilarEntityes,findFocusedEntities
from ERtasks.models import crowdCora


def hello(request):
    return HttpResponse("Hello world ! ")

def dextra(request):
    return render(request, 'dextra/attredit.html')

@login_required
def exploration(request):
    # if request.method == 'POST':
    #     attribute_editor = request.POST.get("attribute_editor")
    #     _save = request.POST.get("_save")
    #     if _save:
    #         return render(request, 'dextra/add.html',{'data':attribute_editor})
    if request.is_ajax():
        print(request.body)
        print(request.POST)
        searchkey = request.POST.get('searchkey')
        page = request.POST.get('page')
        print(searchkey)
        cora_list = Cora.objects.filter(text__contains=searchkey)
        print(cora_list)
        paginator = Paginator(cora_list, 10)
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
            cora_list = Cora.objects.filter(text__contains=searchkey)
            # request.session['q'] = searchkey
        else:
            # searchkey = request.session['q']
            # if searchkey:
            #     cora_list = Cora.objects.filter(text__contains=searchkey)
            # else:
            #     cora_list = Cora.objects.all
            cora_list = Cora.objects.all()
        print(searchkey)
        paginator = Paginator(cora_list,10) # Show 10 per page

        page = request.GET.get('page')
        try:
            cora = paginator.page(page)
        except PageNotAnInteger:
         # first page
            cora = paginator.page(1)
        except EmptyPage:
        # last page
            cora = paginator.page(paginator.num_pages)
        return render(request, 'dextra/exploration.html',{'data': cora,'searchkey':searchkey})

@login_required
def add(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    print(data[0])
    if request.method == 'POST':
        attrname = request.POST.get('attrname')
        scope = request.POST.get('is_local')
        print(attrname, scope)
        models.CoraAttr.objects.create(attrname=attrname, attrscope=scope, is_alive=1, userid=data[0])
        msg = {"attrname": attrname}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.attributeCreate, operate_user=data[0])
    return render(request, 'dextra/add.html')

@login_required
def addvalue(request):

    if request.method == 'POST':
        username = request.session['username']
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        print(uids[0])
        seleattr = request.POST.get("seleattr")
        print("seleattr")
        print(seleattr)
        value = request.POST.get("attrvalue")
        attrsynonym = request.POST.get("attrsynonym")
        print(value,attrsynonym)
        # models.CoraAttrValue.objects.create(attr_id=seleattr,value=value,userid=uids[0])
        val = models.CoraAttrValue(attr_id=seleattr,value=value,userid=uids[0])
        val.save()
        # values = models.CoraAttrValue.objects.filter(value=value)
        # print(values[0].id)
        # models.CoraValueSynonym.objects.create(value=values[0],synonym=attrsynonym,userid=uids[0])
        corasyno = models.CoraValueSynonym(value=val,synonym=attrsynonym,userid=uids[0])
        corasyno.save()
        msg = {"attr_id":seleattr,"value":value,"synonym":attrsynonym}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora,operate_message=json.dumps(msg), operate_flag=dxaconstants.WorkerOperation.valueBind,operate_user=uids[0])
        llist = Cora.objects.filter(attributedtext__contains=attrsynonym)
        attra = models.CoraAttr.objects.get(id=seleattr)
        restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
        for entiy in llist:
            entiy.attributedtext = entiy.attributedtext.replace(attrsynonym,restr)
            entiy.save()
            models.CoraToAttrEntity.objects.create(cora=entiy,attrsynonym=corasyno)
    data = models.CoraAttr.objects.all()
    return render(request, 'dextra/addvalue.html', {'data': data})

@login_required
def addsynonym(request):
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
        valuelist = models.CoraAttrValue.objects.filter(attr_id=test).values('id','value')
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
        username = request.session['username']
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        value = request.POST.get("seleval")
        print('value:',value)
        attrsynonym = request.POST.get("attrsynonym")
        print(attrsynonym)
        # models.CoraValueSynonym.objects.create(value_id=value, synonym=attrsynonym, userid=uids[0])
        corasyno = models.CoraValueSynonym(value_id=value, synonym=attrsynonym, userid=uids[0])
        corasyno.save()
        msg = {"value_id": value, "synonym": attrsynonym}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.valueBind, operate_user=uids[0])
        llist = Cora.objects.filter(attributedtext__contains=attrsynonym)
        seleattr = request.POST.get("attrname")
        attra = models.CoraAttr.objects.get(id=seleattr)
        restr = '<details><summary><span class="summaryText">'+attra.attrname+'</span></summary><p class = "detailtext">'+attrsynonym+'</p></details>'
        for entiy in llist:
            entiy.attributedtext = entiy.attributedtext.replace(attrsynonym,restr)
            entiy.save()
            models.CoraToAttrEntity.objects.create(cora=entiy, attrsynonym=corasyno)
    data = models.CoraAttr.objects.all()
    return render(request, 'dextra/addsynonym.html', {'data': data})

@login_required
def attrmanage(request):
    username = request.session['username']
    data = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
    print(data[0])
    if request.method == 'POST':
        attrname = request.POST.get('attrname')
        scope = request.POST.get('is_local')
        print(attrname, scope)
        models.CoraAttr.objects.create(attrname=attrname, attrscope=scope, is_alive=1, userid=data[0])
        msg = {"attrname": attrname}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.focusedEntityRefinement, operate_user=data[0])
        #return render(request, 'dextra/attrmanage.html')
    meattr = models.CoraAttr.objects.filter(userid=data[0])
    otherattr = models.CoraAttr.objects.exclude(userid=data[0])
    return render(request, 'dextra/attrmanage.html',{'meattr': meattr, 'otherattr': otherattr})

fc = 0
def clusterrefine(request):
    focusedentities = findFocusedEntities(10)
    # request.session['fc'] = 0
    # fc = 0
    global fc
    if request.method == 'POST':
        multis = request.POST.getlist("Entities")
        # get the id of focusedentity
        crcora = crowdCora.objects.filter(cora_id=focusedentities[fc])
        if crcora:
            cluid = crcora[0].clusterid
        else:
            cluid = fc
            crowdCora.objects.create(cora_id=focusedentities[fc], testsystem=dxaconstants.TestSystems.DEXTRA, clusterid=cluid)
        print(multis)
        for i in multis:
            print(i)
            crowdCora.objects.create(cora_id=i, testsystem=dxaconstants.TestSystems.DEXTRA,
                                     clusterid=cluid)
        msg = {"focused_id": focusedentities[fc], "selectedentities": multis}
        username = request.session['username']
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.focusedEntityRefinement, operate_user=uids[0])

        # if request.POST.has_key("_save"):
        #     print("_save")
        # elif request.POST.has_key("_addanother"):
        #     print("_addanother")
        # else:
        #     print("_continue")


        submittype = request.POST.get("submit")
        print(submittype)
        if submittype == "Save":
            print("Save")
        elif submittype == "Save and check another":
            print("Save and check another")
            # fc = request.session['fc']
            if fc < len(focusedentities)-1:
                fc = fc+1
                # request.session['fc'] = fc
            # del focusedentities[0]
        else:
            print("Save and continue editing")


        similar = findSimilarEntityes(focusedentities[fc],20)
        # focus = focusedentities[0].attributedtext.replace('<details>', '<details open="open">')
        focus = Cora.objects.get(id=focusedentities[fc]).attributedtext.replace('<details>', '<details open="open">')
        data = {"focus": focus, 'similar': similar}
        print('fc:',fc)
        return render(request, 'dextra/clusterrefine.html', data)
    similar = findSimilarEntityes(focusedentities[fc],20)
    for s in similar:
        print(s.attributedtext)
    focus = Cora.objects.get(id=focusedentities[fc]).attributedtext.replace('<details>', '<details open="open">')
    data = {"focus": focus,'similar':similar}
    return render(request, 'dextra/clusterrefine.html',data)

def p2(request):
    if request.method == "GET":
        attribute_editor = request.GET.get('attribute_editor')
        aa = request.GET.get('attr')
        print(aa)
        print(attribute_editor)
        return render(request, "dextra/p2.html", {'data': attribute_editor})
    return render(request, "dextra/p2.html")