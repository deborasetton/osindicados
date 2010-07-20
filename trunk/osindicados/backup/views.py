# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from subprocess import PIPE, Popen
import os

@login_required
@csrf_exempt
def index(request):
    # tela de opções
    if request.method == "GET":
        #form_up = UploadFileForm(request.POST, request.FILES)
        #return render_to_response('backup/index.html', {"form_up": form_up})
        return render_to_response('backup/index.html')
    if request.method == "POST":
        # opção selecionada = download do banco
        if request.POST["mode"] == "download":
            nome ="teste.json" #TODO
            print os.listdir('.')
            saida = Popen(["python", "manage.py", "dumpdata"], stdout=PIPE).communicate()[0]
            response = HttpResponse(saida, mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + nome
            return response
        # opcao selecionada = upload do banco
        if request.POST["mode"] == "upload":
            print request.FILES
            f = request.FILES["file"]
            for chunk in f.chunks():
                print chunk
            return HttpResponse("Upload OK")