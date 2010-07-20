# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from subprocess import PIPE, Popen
import os
import subprocess

@login_required
@csrf_exempt
def index(request):
    # tela de opções
    if request.method == 'GET':
        #form_up = UploadFileForm(request.POST, request.FILES)
        #return render_to_response('backup/index.html', {'form_up': form_up})
        return render_to_response('backup/index.html')
    if request.method == 'POST':
        # opção selecionada = download do banco
        if request.POST['mode'] == 'download':
            nome ='teste.json' #TODO
            print os.listdir('.')
            saida = Popen(['python', 'manage.py', 'dumpdata'], stdout=PIPE).communicate()[0]
            response = HttpResponse(saida, mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + nome
            return response
        # opcao selecionada = upload do banco
        if request.POST['mode'] == 'upload':
            #guarda arquivo recebido
            f = request.FILES['file']
            destination = open('backup\\backup_data\\' + f.name, 'wb+')
            print destination.name
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            #verificar se eh possível realizar loaddata com arquivo recebido

            #limpa o banco
            saida = Popen(['python', 'manage.py', 'flush', '--noinput'], stdout=PIPE).communicate()[0]
            print saida
            #recupera backup usando o arquivo recebido
            saida = Popen(['python', 'manage.py', 'loaddata', destination.name], stdout=PIPE).communicate()
            print 'saida:'
            print saida[0]
            print saida[1]

            # verifica se comando anterior retornou erro
            if saida[0] != '': #TODO: isso não é suficiente... =(
                #deleta arquivo
                os.remove(destination.name)
                return HttpResponse('Upload realizado com sucesso! saida:')
            else:
                # não foi possivel realizar loaddata.
                return HttpResponse('ERRO AO REALIZAR UPLOAD')