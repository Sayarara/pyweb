from DEXTRA import precluster
from ERtasks.models import Cora
from baselinededupe import models
import json
import ast

def findNearestClusters(focusedentityid,num):
    coras = models.clusterCanonicalRepresentation.objects.all()
    dic = {}
    ss = []
    mhfocused = precluster.mh(Cora.objects.get(id=focusedentityid).text.split(' '))
    for ca in coras:
        # print(ca.canonrep)
        ca_canonrep = ast.literal_eval(ca.canonrep)
        mhca = precluster.mh(ca_canonrep['text'].split(' '))
        dic[ca.id] = precluster.mhJC(mhfocused, mhca)
    list_sort_value_desc = precluster.sort_dict(dic)
    # print(list_sort_value_desc[15:15 + num])

    for d in list_sort_value_desc[0:0 + num]:
        # print(d)
        # print(d[0])
        a = models.clusterCanonicalRepresentation.objects.get(id=d[0])
        ca_canonrep = ast.literal_eval(a.canonrep)
        temp = {"clusterid":a.clusterid,"can_rep":ca_canonrep['text']}
        # print(temp)
        ss += [temp]
    return ss

