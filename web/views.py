# coding=utf-8
#
#  views.py
#  myAssistant
#
#  Created by bin on 14/11/18.
#  Copyright (c) 2014年 bin. All rights reserved.
#

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from web.models import Records
import datetime
import time


@csrf_exempt
def synchrony(request):
    if request.method == 'POST':
        json = request.POST.get('json', '')
        synchronyArray = simplejson.loads(json)['synchronyArray']
        for synchronyRecord in synchronyArray:
            modify = synchronyRecord['modify']
            id = synchronyRecord['id']
            time = synchronyRecord['time']
            year = synchronyRecord['year']
            month = synchronyRecord['month']
            day = synchronyRecord['day']
            content = synchronyRecord['content']

            if modify == 'A':
                newRank = Records(year=year, month=month, day=day, time=time, content=content, needsynchrony=1)
                newRank.save()
            if modify == 'D':
                try:
                    Records.objects.filter(id=id).delete()
                except Exception, e:
                    print e
            # 修改
            if modify == 'M':
                rows = Records.objects.filter(id=id)
                if rows:
                    record = rows[0]
                    record.time = time
                    record.year = year
                    record.month = month
                    record.day = day
                    record.content = content
                    record.needsynchrony = 1
                    record.save()
                else:
                    print "找不到记录,新增"
                    newRank = Records(year=year, month=month, day=day, time=time, content=content, needsynchrony=1)
                    newRank.save()

        # 返回
        allRecords = Records.objects.all()
        allIndexList = []
        synchronyList = []
        for record in allRecords:
            allIndexList.append(record.id)
        synchronyRecords = Records.objects.filter(needsynchrony=1)
        for record in synchronyRecords:
            synchronyList.append({'id':record.id, 'year':record.year, 'month':record.month, 'day':record.day, 'time':record.time, 'content':record.content})
            record.needsynchrony = 0
            record.save()

        JsonData = simplejson.dumps({'state':'1', 'allIndexList':allIndexList, 'synchronyList':synchronyList}, ensure_ascii=False)
        return HttpResponse(JsonData)
        # except:
        #     JsonData = simplejson.dumps({'state':'0', 'content':'error'}, ensure_ascii=False)
        #     return HttpResponse(JsonData)


def assistantPage(request):
    allRecords = Records.objects.all()
    displayRecordList = []
    for record in allRecords:
        displayRecord = {}
        displayRecord['date'] = datetime.datetime(record.year, record.month, record.day).strftime("%Y-%m-%d")
        displayRecord['start'] = displayRecord['date'] + 'T' + record.time
        displayRecord['title'] = record.content
        displayRecord['time'] = record.time
        displayRecord['id'] = record.id
        displayRecord['format'] = datetime.datetime(record.year, record.month, record.day).strftime("%m %d %Y ") + record.time
        displayRecordList.append(displayRecord)
    displayRecordList = simplejson.dumps(displayRecordList)
    currentMonth = time.strftime('%Y-%m',time.localtime(time.time()))
    # print displayRecordList
    return render_to_response('main.html', {"displayRecordList":displayRecordList, "currentMonth":currentMonth}, context_instance=RequestContext(request))


@csrf_exempt
def update(request):
    # print request.POST
    operationType = request.POST.get('operationType', '')
    if operationType == 'M':
        modifyList = request.POST.getlist('modifyList[]')
        for modifyRow in modifyList:
            modifyRow = modifyRow.split('-split-')
            rows = Records.objects.filter(id=modifyRow[0])
            if rows:
                record = rows[0]
                record.time = modifyRow[1]
                record.content = modifyRow[2]
                record.needsynchrony = 1
                record.save()
        delectList = request.POST.getlist('delectList[]', '')
        for deleteRow in delectList:
            try:
                Records.objects.filter(id=deleteRow).delete()
            except Exception, e:
                print e
        return HttpResponse(simplejson.dumps({'state':'1'}))
    if operationType == 'A':
        dateTime = request.POST.get('date')
        content = request.POST.get('content')
        date = time.strptime(dateTime, "%Y-%m-%d %H:%M") 
        dtime = dateTime.split(' ')[1]
        newRank = Records(year=date.tm_year, month=date.tm_mon, day=date.tm_mday, time=dtime, content=content, needsynchrony=1)
        newRank.save()
        return HttpResponse(simplejson.dumps({'state':'1'}))
    return HttpResponse(simplejson.dumps({'state':'0'}))



