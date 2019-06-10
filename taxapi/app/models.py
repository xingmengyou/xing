# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WjzInfo(models.Model):
    ywid = models.CharField(max_length=255, blank=True, null=True)
    jd = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    money = models.FloatField()
    phone = models.CharField(max_length=128)
    agent = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    begindate = models.CharField(max_length=64)
    enddate = models.CharField(max_length=64)
    validity = models.CharField(max_length=128, blank=True, null=True)
    documenturl = models.TextField(blank=True, null=True)
    managenum = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'wjz_info'
