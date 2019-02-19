from django.db import models

# Create your models here.

class Cora(models.Model):
    entityurl = models.CharField(max_length=128)
    text = models.TextField()
    attributedtext = models.TextField(default=text)

class Cora_labeled(models.Model):
    entityurl = models.CharField(max_length=128)
    text = models.TextField()
    labeledtext = models.TextField(default=text)
    cleantext = models.TextField(default=text)
    orderscore = models.FloatField(default=0)

class crowdCora(models.Model):
    cora = models.ForeignKey(Cora, on_delete=models.CASCADE)
    testsystem = models.CharField(max_length=128)
    clusterid = models.IntegerField(default=0)

class clusterCora(models.Model):
    cora = models.ForeignKey(Cora, on_delete=models.CASCADE)
    testsystem = models.CharField(max_length=128)
    clusterid = models.IntegerField(default=0)
    confidence = models.FloatField()
    user = models.CharField(max_length=128)
    is_checked = models.IntegerField(default=-1)
