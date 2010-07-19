# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen
from subprocess import PIPE
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def index(request):
    # tela de opções
    if request.method == "GET":
        return render_to_response('backup/index.html')
    if request.method == "POST":
        # opção selecionada = download do banco
        if request.POST["mode"] == "download":
            nome ="teste.backup" #TODO
            print os.listdir('.')
            saida = Popen(["python", "manage.py", "dumpdata"], stdout=PIPE).communicate()[0]
            response = HttpResponse(saida, mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + nome
            return response

