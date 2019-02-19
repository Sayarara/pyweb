from DEXTRA import precluster
from ERtasks.models import Cora
from  django.db.models import  Q
from  django.db.models import Count

def searchmh(kw,seedid,num):

    print(kw)
    kws= kw.split(',')
    print('searchmh---------------------------------------')
    print(kws)
    # if len(kws) == 3:
    #     print("kws:",len(kws))
    #     coras = Cora.objects.filter(Q(text__contains=kws[0])|Q(text__contains=kws[1])|Q(text__contains=kws[2]))
    # else:
    #     coras = Cora.objects.all()
    coras = Cora.objects.all()
    dic = {}
    ss = []
    print("seed text")
    print(Cora.objects.get(id=seedid).text)
    mhfocused = precluster.mh(Cora.objects.get(id=seedid).text)
    for ca in coras:
        mhca = precluster.mh(ca.text)
        dic[ca.id] = precluster.mhJC(mhfocused, mhca)
        # print(dic[ca.id])
    list_sort_value_desc = precluster.sort_dict(dic)
    if len(list_sort_value_desc) <= num:
        al = list_sort_value_desc
    else:
        al = list_sort_value_desc[:num]
    for d in al:
        print(d)
        print(d[0])
        a = Cora.objects.get(id=d[0])
        print(a)
        ss += [a]
    return ss

def findtail():
    groups = Cora.objects.values_list("entityurl").annotate(groupSize=Count("id")).order_by("groupSize")
    tail = []
    tailcoras = []
    for d in groups:
        tail.append(d[0])
        print(d[0],d[1])
        if d[1] > 3:
            break
            print(d)

    print(tail)
    for eee in tail:
        crs = Cora.objects.filter(entityurl=eee)
        for cr in crs:
            tailcoras.append(cr.id)
    print(tailcoras)
    return tailcoras