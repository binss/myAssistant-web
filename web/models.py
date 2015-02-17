#coding=utf-8
#
#  models.py
#  myAssistant
#
#  Created by bin on 14/11/18.
#  Copyright (c) 2014年 bin. All rights reserved.
#

from django.db import models

class Records(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    time = models.CharField(max_length=20L)
    content = models.CharField(max_length=255L)
    needsynchrony = models.IntegerField(db_column='needSynchrony') # Field name made lowercase.
    class Meta:
        db_table = 'RECORDS'