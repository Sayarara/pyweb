from  django.db.models import Count
from ERtasks.models import Cora
from DEXTRA import models
from DEXTRA import precluster
from datasketch.minhash import MinHash

def findFocusedEntities(num):
    groups = Cora.objects.values_list("entityurl").annotate(groupSize=Count("id")).order_by("groupSize").reverse()
    ss = []
    for d in groups[15:15+num]:
        print(d)
        print(d[0])
        ds = Cora.objects.filter(entityurl=d[0])[0]
        print(ds.id)
        ss += [ds.id]
    # print(groups)
    # co = [d[0] for d in groups[:num]]
    # print(co)
    return ss

def findSimilarEntityes(focusedentityid,num):
    _t = models.CoraToAttrEntity.objects.filter(cora_id=focusedentityid)
    ss = []
    if _t:
        print('')
    else:
        coras = Cora.objects.all()
        dic = {}
        mhfocused = precluster.mh(Cora.objects.get(id=focusedentityid).text.split(' '))
        for ca in coras:
            mhca = precluster.mh(ca.text.split(' '))
            dic[ca.id] = precluster.mhJC(mhfocused,mhca)
            print(dic[ca.id])
        list_sort_value_desc = precluster.sort_dict(dic)
        print(list_sort_value_desc[15:15+num])

        for d in list_sort_value_desc[0:0+num]:
            print(d)
            print(d[0])
            a = Cora.objects.get(id=d[0])
            print(a)
            ss += [a]
    return ss