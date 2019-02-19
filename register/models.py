from django.db import models

from django.utils import timezone
from pyweb import  dxaconstants
# Create your models here.

class WorkerInfo(models.Model):
    user = models.CharField(max_length=128)
    pwd = models.CharField(max_length=128)
    domain = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    hobby = models.CharField(max_length=128)

class WorkLog(models.Model):
    operate_time = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    operate_message = models.TextField(blank=True)
    task = models.CharField(max_length=128)
    operate_flag = models.CharField(max_length=128)
    operate_user = models.CharField(max_length=128)
    operate_system = models.CharField(max_length=128)



