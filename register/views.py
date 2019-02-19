from django.shortcuts import render
from  django.shortcuts import redirect
from django.shortcuts import HttpResponse
# Create your views here.
from register import models
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:

            # 设置session内部的字典内容
            request.session['is_login'] = 'true'
            request.session['username'] = username
            login(request, user)
            # Redirect to a success page.
            #return render(request, 'welcome.html', {'data': data[0]})
            return redirect('/welcome/')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {
                'data': "Please enter the correct username and password for your account.Note that both fields may be case-sensitive."})
    return render(request, 'login.html')


def register(request):
    #return HttpResponse('Hello World')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        domain = request.POST.get('domain')
        role = request.POST.get('role')
        hobby = request.POST.get('hobby')
        models.WorkerInfo.objects.create(user=username,pwd=password,domain=domain,role=role,hobby=hobby)
        User.objects.create_user(username=username, password=password, is_staff=1)

        return redirect('/accounts/login/')
        #return render(request, 'login.html')
    return render(request, 'register.html')

def login2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        passwd = models.WorkerInfo.objects.get(user=username).pwd
        if password == passwd:
            request.session['username'] = username
            request.session.set_expiry(600)
            return render(request, 'welcome.html')
        else:
            return render(request, 'login.html', {'data': "Please enter the correct username and password for your account.Note that both fields may be case-sensitive."})
    return render(request, 'login.html')



def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username, password)

        a=models.WorkerInfo.objects.filter(user=username).filter(pwd=password).count()

        print(a)
        tag = a == 1


        if tag:
            data=models.WorkerInfo.objects.filter(user=username)
            print(data)
            for aa in data:
                print(aa.user, aa.domain)
            print(data[0].user,data[0].hobby)
            #return render(request, 'welcome.html', {'data': username})
            return render(request, 'welcome.html', {'data': data[0]})
        else:
            #data_list = []
            temp = {'tag': a != 1,'str':"Please enter the correct username and password for a staff account.Note that both fields may be case-sensitive."}
            #data_list.append(temp)
            return render(request, 'login.html', {'data': temp})
        #temp = {'user': username, 'pwd': password}
        #user_list.append(temp)
        # 将数据保存到数据库

    return render(request, 'login.html')




@login_required
def welcome(request):
    #return HttpResponse('Hello World')
    username = request.session['username']
    data = models.WorkerInfo.objects.filter(user=username)
    print(data)
    for aa in data:
        print(aa.user, aa.domain)
    print(data[0].user, data[0].hobby)
    #return render(request, 'welcome.html')
    return render(request, 'welcome.html', {'data': data[0]})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

@login_required
def change_password(request):
    if request.method == 'POST':
        oldPassword = request.POST.get('old_password')
        newPassword1 = request.POST.get('new_password1')
        newPassword2 = request.POST.get('new_password2')
        if request.user.check_password(oldPassword):
            request.user.set_password(newPassword1)
            request.user.save()
            result = {'status': 0, "info": "密码修改登录成功！！"}
        else:
            result = {'status': 1, "info": "原密码不正确！！"}
        return HttpResponse(result)
    # if request.is_ajax():
    #     data = json.loads(request.POST.get('data'))
    #     oldPassword = data.get('oldPassword')
    #     newPassword = data.get('newPassword')
    #     confirmPassword = data.get('confirmPassword')
    #     if request.user.check_password(oldPassword):     # 判断旧密码是否正确
    #         request.user.set_password(newPassword)
    #         request.user.save()
    #         result = {'status': 0, "info": "密码修改登录成功！！"}
    #     else:
    #         result = {'status': 1, "info": "原密码不正确！！"}
    #     return HttpResponse(json.dumps(result))
    return render(request, 'password_change.html')