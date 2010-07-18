# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def index(request):
    if request.method == "GET":
        return render_to_response('backup/index.html')
