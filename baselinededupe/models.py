from django.db import models
from ERtasks.models import Cora

# Create your models here.
class uncertainpiars(models.Model):
    id1 = models.IntegerField()
    text1 = models.TextField()
    id2 = models.IntegerField()
    text2 = models.TextField()
    task = models.CharField(max_length=128)
    is_same = models.IntegerField(default=-1)
    user = models.CharField(max_length=128)

class blocking_map(models.Model):
    block_key = models.CharField(max_length=200)
    data_id = models.IntegerField()

class clusterTemp(models.Model):
    task_record_id = models.IntegerField()
    task = models.CharField(max_length=128)
    clusterid = models.IntegerField(default=0)
    confidence = models.FloatField()
    user = models.CharField(max_length=128)

class clusterCanonicalRepresentation(models.Model):
    clusterid = models.IntegerField()
    canonrep = models.TextField()
    task = models.CharField(max_length=128)
    user = models.CharField(max_length=128)

