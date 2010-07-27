# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from subprocess import PIPE, Popen
import datetime
import os

class UploadFileForm(forms.Form):
    file  = forms.FileField()

@login_required
@csrf_exempt
def index(request):
    # tela de opções
    if request.method == 'GET':
        form_up = UploadFileForm()
        #form_up = UploadFileForm(request.POST, request.FILES)
        return render_to_response('backup/index.html', {'form_up': form_up, 'user': request.user})
        #return render_to_response('backup/index.html')
    if request.method == 'POST':
        # opção selecionada = download do banco
        if request.POST['mode'] == 'download':
            now =  datetime.datetime.now()
            nome = 'banco_osindicados_' + now.strftime("%Y-%m-%d_%Hh%Mm%Ss") +'.json'
            print os.listdir('.')
            saida = Popen(['python', 'manage.py', 'dumpdata', '--natural'], stdout=PIPE).communicate()[0]
            response = HttpResponse(saida, mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + nome
            return response
        # opcao selecionada = upload do banco
        if request.POST['mode'] == 'upload':
            form_up = UploadFileForm(request.POST, request.FILES)
            if form_up.is_valid():
                #faz backup de segurança do banco
                saida = Popen(['python', 'manage.py', 'dumpdata', '--natural'], stdout=PIPE).communicate()[0]
                security_backup = open('backup\\backup_data\\' + 'security_backup.json', 'wb+')
                security_backup.write(saida)
                security_backup.close()
                #guarda arquivo recebido
                f = request.FILES['file']
                destination = open('backup\\backup_data\\' + f.name, 'wb+')
                print destination.name
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
                #limpa o banco
                Popen(['python', 'manage.py', 'flush', '--noinput'], stdout=PIPE).communicate()
                #recupera backup usando o arquivo recebido
                saida = Popen(['python', 'manage.py', 'loaddata', destination.name], stdout=PIPE).communicate()
                #deleta arquivo
                os.remove(destination.name)
                # verifica se a recuperacao eh valida (verifica se existe pelo menos um usuario cadastrado no sistema
                if len(User.objects.all()) > 0:
                    #reguperacao valida
                    return HttpResponse('Upload realizado com sucesso! saida:' + saida[0])
                else:
                    # não foi possivel realizar loaddata.
                    #recupera estado anterior
                    print "recuperando backup de seguranca"
                    Popen(['python', 'manage.py', 'flush', '--noinput'], stdout=PIPE).communicate()
                    Popen(['python', 'manage.py', 'loaddata', security_backup.name], stdout=PIPE).communicate()
                    return render_to_response('backup/index.html', {'form_up': form_up, 'mensagem_err': 'ERRO AO REALIZAR UPLOAD, nenhuma alteracao foi realizada. Verifique se o arquivo selecionado corresponde a um backup feito anteriormente'})
            else:
                # form invlido
                return render_to_response('backup/index.html', {'form_up': form_up, 'mensagem_err': "Escolha um arquivo no seu computador antes de clicar em 'Upload'"})