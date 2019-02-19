from django.db import models
from ERtasks.models import Cora

# Create your models here.

class patternSeedTemp(models.Model):
    seedsubstring = models.TextField()
    user = models.CharField(max_length=128,default='')




class sigirAttrExploration(models.Model):
    substring = models.CharField(max_length=128)
    orderscore = models.FloatField()
    is_labelled = models.BooleanField(default=False)
    user = models.CharField(max_length=128,default='aming')

class sigirCoraAttr(models.Model):
    attrname = models.CharField(max_length=128)
    attrscope = models.CharField(max_length=128)
    is_alive = models.BooleanField()
    userid = models.IntegerField()

class sigirCoraAttrValue(models.Model):
    attr = models.ForeignKey(sigirCoraAttr, on_delete=models.CASCADE)
    value = models.CharField(max_length=300)
    userid = models.IntegerField(default=0)

class sigirCoraValueSynonym(models.Model):
    value = models.ForeignKey(sigirCoraAttrValue, on_delete=models.CASCADE)
    synonym = models.CharField(max_length=300)
    userid = models.IntegerField(default=0)

class sigirCoraToAttrEntity(models.Model):
    cora = models.ForeignKey(Cora, on_delete=models.CASCADE)
    attrsynonym = models.ForeignKey(sigirCoraValueSynonym, on_delete=models.CASCADE)
    user = models.CharField(max_length=128,default='aming')
# Create your models here.

class CoraPerformanceLog(models.Model):
    cora = models.ForeignKey(Cora, on_delete=models.CASCADE)
    clusterid = models.IntegerField(default=0)
    confidence = models.FloatField()
    explorationMethod = models.CharField(max_length=128)
    workerOperationNum = models.IntegerField(default=0)


class piars(models.Model):
    id1 = models.IntegerField()
    text1 = models.TextField()
    id2 = models.IntegerField()
    text2 = models.TextField()
    samplingMethod = models.CharField(max_length=128)
    task = models.CharField(max_length=128)
    is_same = models.IntegerField(default=-1)
    user = models.CharField(max_length=128)

class MultiItems(models.Model):
    seedid = models.IntegerField()
    text1 = models.TextField()
    keywords = models.TextField(blank=True)
    candidateidset = models.TextField(blank=True)
    selectedidset = models.TextField(blank=True)
    samplingMethod = models.CharField(max_length=128)
    task = models.CharField(max_length=128)
    is_checked = models.IntegerField(default=-1)
    user = models.CharField(max_length=128)

class dextraitems(models.Model):
    attrname = models.CharField(max_length=128)
    msg = models.TextField(blank=True)
    samplingMethod = models.CharField(max_length=128)
    task = models.CharField(max_length=128)
    optype = models.CharField(max_length=128)
    user = models.CharField(max_length=128)

class sigirSynonymsSeedTemp(models.Model):
    cattr = models.ForeignKey(sigirCoraAttr, on_delete=models.CASCADE)
    user = models.CharField(max_length=128,default='aming')