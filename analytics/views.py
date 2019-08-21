from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import AnalyticsItem
from .analyticstool import *

def analyticsView(request):
	allItems = AnalyticsItem.objects.all()
	return render(request, 'analytics.html',
		{'allItems': allItems})

def addAnalytics(request):
	subreddit = request.POST['subreddit']
	keyword = request.POST['keyword']
	newItem = AnalyticsItem(content=keyword)
	newItem.save()
	plotGraph(subreddit, keyword) 
	return HttpResponseRedirect('/analytics/')