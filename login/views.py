from django.shortcuts import render
from django.shortcuts import HttpResponse
from login import models
from DEXTRA.precluster import preclusterTest
from DEXTRA.explore import attrexplore
# Create your views here.
import json

#user_list = []

def index(request):
    #return HttpResponse('Hello World')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        #temp = {'user': username, 'pwd': password}
        #user_list.append(temp)
        # 将数据保存到数据库
        models.UserInfo.objects.create(user=username, pwd=password)
    # 从数据库中读取所有数据，注意缩进
    user_list = models.UserInfo.objects.all()
    return render(request, 'index.html', {'data': user_list})
    #return render(request, 'index.html', {'data': user_list})




import json


def ajax_submit(request):
    if request.is_ajax():
        print(request.body)
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        ret = {'status': 0, "msg": "aaabjaojwoftjwo"}
        groups = preclusterTest()

        for d in  groups[:5]:
            print(d)
            print(d[0])
        print(groups)
        co = [d[0] for d in  groups[:5]]
        print(co)
        # corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
        #           "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
        #           "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
        #           "我 爱 北京 天安门"]  # 第四类文本的切词结果
        corpus = ['this is sentence one','this is sentence two','this is sentence three']

        attrexplore(corpus)
        return HttpResponse(json.dumps(ret))
    return render(request, "ajax_submit.html")

