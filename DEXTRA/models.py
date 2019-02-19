from django.db import models
from ERtasks.models import Cora

# Create your models here.

class CoraAttr(models.Model):
    attrname = models.CharField(max_length=128)
    attrscope = models.CharField(max_length=128)
    is_alive = models.BooleanField()
    userid = models.IntegerField()

class CoraAttrValue(models.Model):
    attr = models.ForeignKey(CoraAttr, on_delete=models.CASCADE)
    value = models.CharField(max_length=300)
    userid = models.IntegerField(default=0)

class CoraValueSynonym(models.Model):
    value = models.ForeignKey(CoraAttrValue, on_delete=models.CASCADE)
    synonym = models.CharField(max_length=300)
    userid = models.IntegerField(default=0)

class CoraToAttrEntity(models.Model):
    cora = models.ForeignKey(Cora, on_delete=models.CASCADE)
    attrsynonym = models.ForeignKey(CoraValueSynonym, on_delete=models.CASCADE)

