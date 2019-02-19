from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ERtasks.models import Cora,crowdCora
from baselinealloy.castgather import searchmh,findtail
from DEXTRA.clusterrefine import findSimilarEntityes
# Create your views here.
import random
from django.http import HttpResponse
import json
from baselinealloy import models
from register.models import WorkerInfo, WorkLog
from pyweb import dxaconstants


@login_required
def alloy2(request):
    seed1 = Cora.objects.order_by('?')[:4]
    cou = 1
    data = {}
    for i in seed1:
        strr = "seed"+str(cou)
        data[strr] = i
        # similar = findSimilarEntityes(i.id, 9)
        # strr = "similar"+str(cou)
        # data[strr] = similar
        cou = cou+1
    print(data)
    if request.is_ajax():
        print(request.body)
        print(request.POST)
        print('ajax')
        seed1kw = request.POST.get("seed1kw")
        seedid = request.POST.get("seedid")
        print(seed1kw)
        print(seedid)
        if seed1kw:
            similar = searchmh(kw=seed1kw,seedid=data['seed1'].id,num=9)
            print(similar)


    return render(request, 'alloy/headcast.html',data)


def alloy(request):
    if request.method == 'POST':
        username = request.session['username']
        multis = request.POST.getlist("Records")
        pseedid = request.POST.get("pseedid")
        print(pseedid)

        # crowdCora.objects.create(cora_id=focusedentities[fc], testsystem=dxaconstants.TestSystems.DEXTRA,
        #                          clusterid=cluid)

    if request.is_ajax():
        print('ajax')
        seed1kw = request.POST.get("seed1kw")
        print(seed1kw)
        # seedid = request.POST.get("seedid")
        seedid = models.CoraTemp.objects.get(id=1).currentCora_id
        print(seedid)
        cora = Cora.objects.get(id=seedid)
        htmlstr = ""
        if seed1kw:
            print(True)
            similar = searchmh(kw=seed1kw,seedid=seedid,num=9)
            print(similar)
            for i in similar:
                htmlstr = htmlstr + "<option value='" + str(i.id) + "'>" + i.text + "</option>"
        #data = {'valuestr': htmlstr,'cora':cora}
        data = {'valuestr': htmlstr.encode('utf8')}
        print(data)
        return HttpResponse(json.dumps(data))

    fc = 0
    print('not ajax')
    seed = Cora.objects.order_by('?')[:4]
    print(seed)
    print(seed[fc].id)
    current = models.CoraTemp.objects.get(id=1)
    print(current.currentCora)
    current.currentCora = seed[fc]
    current.save()
    # similar = searchmh(kw="", seedid=seed[fc].id, num=9)
    #similar = findSimilarEntityes(seed[fc].id, 9)
    # data = {'seed': seed[fc],'similar':similar}
    data = {'seed': seed[fc]}
    return render(request, 'alloy/headcast.html',data)



def tailcast(request):
    if request.method == 'POST':
        is_same = request.POST.get('is_same')
        print(is_same)
        ts = models.tail.objects.filter(is_same=-1).order_by("id")
        t = ts[0]
        t.is_same = is_same
        username = request.session['username']
        uids = WorkerInfo.objects.filter(user=username).values_list('id', flat=True)
        t.user_id = uids[0]
        t.save()
        msg = {"cora1_id": t.cora1_id, "cora2_id": t.cora2_id,"is_same":is_same}
        WorkLog.objects.create(task=dxaconstants.ERTASK.Cora, operate_message=json.dumps(msg),
                               operate_flag=dxaconstants.WorkerOperation.pairJudge, operate_user=uids[0],
                               operate_system=dxaconstants.TestSystems.Alloy)
        ts = models.tail.objects.filter(is_same=-1).order_by("id")
        cora1 = Cora.objects.get(id=ts[0].cora1_id)
        cora2 = Cora.objects.get(id=ts[0].cora2_id)
        return render(request, 'alloy/tailcast.html', {"cora1": cora1, "cora2": cora2,'leftpairs':len(ts)})

    # 初始化可能的tail
    if models.tail.objects.all():
        print("has tail")
    else:
        tail = findtail()
        coras = Cora.objects.filter(id__in=tail)
        for i in range(len(coras)):
            for j in range(i + 1, len(coras)):
                models.tail.objects.create(cora1_id=coras[i].id, cora2_id=coras[j].id,user_id=1)
    ts = models.tail.objects.filter(is_same=-1).order_by("id")
    cora1 = Cora.objects.get(id=ts[0].cora1_id)
    cora2 = Cora.objects.get(id=ts[0].cora2_id)
    return render(request, 'alloy/tailcast.html', {"cora1": cora1, "cora2": cora2, 'leftpairs': len(ts)})


def clipmerge(request):
    if request.method == 'POST':
        is_merge = request.POST.get('is_same')
        print(is_merge)

        if is_merge == 1:
            clipclusterid1 = request.POST.get('clipclusterid1')
            clipclusterid2 = request.POST.get('clipclusterid2')
            crowdCora.objects.filter(clusterid=clipclusterid2).update(clusterid=clipclusterid1)
            print(is_merge)

        return render(request, 'alloy/clipmerge.html')
    return render(request,'alloy/clipmerge.html')

