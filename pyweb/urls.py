"""pyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import index
from  login.views import ajax_submit
from register import views
# from DEXTRA.views import dextra
# from DEXTRA.views import add
# from DEXTRA.views import exploration
# from DEXTRA.views import attrmanage
from DEXTRA import views as dextraviews
from baselinealloy import views as alloyviews
from baselinededupe import  views as dedupeviews
from sigirexperiments import views as sigirexpviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('app01/ajax_submit/', ajax_submit),
    path('register/', views.register),
    path('accounts/login/', views.login_view),
    path('welcome/', views.welcome),
    path('logout/', views.logout_view),
    path('password_change/', views.change_password),
    path('dextra/', dextraviews.dextra),
    path('dextra/add', dextraviews.add),
    path('dextra/exploration', dextraviews.exploration),
    path('dextra/addvalue', dextraviews.addvalue),
    path('dextra/addsynonym', dextraviews.addsynonym),
    path('dextra/clusterrefine', dextraviews.clusterrefine),
    path('dextra/dextra/p2', dextraviews.p2),
    path('dextra/p2', dextraviews.p2),
    path('dextra/dextra/exploration', dextraviews.exploration),
    path('dextra/attrmanage', dextraviews.attrmanage),
    path('dextra/attredit', dextraviews.dextra),
    path('alloy/', alloyviews.alloy),
    path('alloy/headcast', alloyviews.alloy),
    path('alloy/tailcast', alloyviews.tailcast),
    path('alloy/clipmerge', alloyviews.clipmerge),
    path('dedupe/activelabel', dedupeviews.activelabel),
    path('dedupe/clusterreview', dedupeviews.clusterreview),
    path('dedupe/addtoclusters', dedupeviews.addtoclusters),
    path('dedupe/polishclusters', dedupeviews.addtoclusters),
    path('sigirexp/exploreperformance', sigirexpviews.exploreperformance),
    path('sigirexp/record_randsampling', sigirexpviews.record_randomsampling),
    path('sigirexp/record_uncertainsampling', sigirexpviews.record_uncertainsampling),
    path('sigirexp/record_searchsampling', sigirexpviews.searchsampling),
    path('sigirexp/add', sigirexpviews.add),
    path('sigirexp/exploration', sigirexpviews.exploration),
    path('sigirexp/addvalue', sigirexpviews.addvalue),
    path('sigirexp/addsynonym', sigirexpviews.addsynonym),
    path('sigirexp/attrexploration', sigirexpviews.attrexploration),
    path('sigirexp/pattern_siblings', sigirexpviews.pattern_siblings),
    path('sigirexp/pattern_synonyms', sigirexpviews.pattern_synonyms),
    path('sigirexp/entityview', sigirexpviews.entityview),
]


