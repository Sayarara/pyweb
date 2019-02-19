from django.db import models
from ERtasks.models import Cora
from register.models import WorkerInfo
# Create your models here.

class CoraTemp(models.Model):
    currentCora = models.ForeignKey(Cora,on_delete=models.CASCADE)


class tail(models.Model):
    # cora1 = models.ForeignKey(Cora,on_delete=models.CASCADE)
    # cora2 = models.ForeignKey(Cora,on_delete=models.CASCADE)
    cora1_id = models.IntegerField()
    cora2_id = models.IntegerField()
    is_same = models.IntegerField(default=-1)
    user = models.ForeignKey(WorkerInfo,on_delete=models.CASCADE)

class head(models.Model):
    # cora1 = models.ForeignKey(Cora,on_delete=models.CASCADE)
    # cora2 = models.ForeignKey(Cora,on_delete=models.CASCADE)
    cora1_id = models.IntegerField()
    cora2_id = models.IntegerField()
    is_same = models.IntegerField(default=-1)
    user = models.ForeignKey(WorkerInfo,on_delete=models.CASCADE)