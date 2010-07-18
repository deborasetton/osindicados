# -*- coding: utf-8 -*-

import random
from osindicados.jogo.models import Tema, Pergunta
from osindicados.jogo.partidaconfs import *
from osindicados.jogo.utils import sortearAlternativas
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from ctypes.wintypes import INT

def index(request):
    temas = Tema.objects.all()
    perguntas = Pergunta.objects.all()

    # calcula quantas perguntas foram cadastradas em cada tema
    list_tema_qntd = [(tema, len(Pergunta.objects.filter(idAssunto__exact=tema.id))) for tema in temas]

    return render_to_response('jogo/index.html', {'list_tema_qntd': list_tema_qntd, 'perguntas': perguntas})

def partida(request):
    """
    Pagina de "Responder Pergunta". Apos configurar o jogo, o usuario e' redirecionado para esta pagina.
    Busca uma nova pergunta e repassa a tela.
    """
    
    # Testa se já existe uma pergunta sendo respondida. Se houver, continua com a mesma. Assim, caso o usuário
    # atualize a página, ele não "ganha" uma ajuda de troca de graça.
    if 'pergunta' in request.session:
        return render_to_response('jogo/partida.html', {'confs': request.session['confs'], 'pergunta' : request.session['pergunta'], 'alternativas' : request.session.get('alternativas'), 'respondidas' : request.session.get('respondidas'), 'ajudas' : request.session.get('ajudas'), 'eliminadas' : request.session.get('eliminadas')}, context_instance=RequestContext(request))

    # Testa se o usuário já passou pela tela de configuração. Se não passou, mostra mensagem de erro.
    if 'confs' in request.session:
        if 'p_ids' in request.session:
            # Nao e' a primeira pergunta. Recupera a lista de ids que ja' foram
            p_ids = request.session['p_ids']
            # Busca uma pergunta nao-repetida
            pergunta = Pergunta.getPerguntaPorAssunto(request.session['confs'].temas, p_ids)
            # Adiciona o id 'a lista
            p_ids.append(pergunta.id)
            # Guarda de volta na sessao
            request.session['p_ids'] = p_ids
        else:
            # E' a primeira pergunta. Busca uma pergunta com qualquer id.
            pergunta = Pergunta.getPerguntaPorAssunto(request.session['confs'].temas)
            # Inicia a lista de ids de perguntas com o id dessa pergunta
            p_ids = [pergunta.id]
            # Adiciona a lista 'a sessao
            request.session['p_ids'] = p_ids
            request.session['respondidas'] = 0
        
        
        mixed = sortearAlternativas(pergunta)
    
        request.session['pergunta'] = pergunta
        request.session['alternativas'] = mixed
        print "Eliminadas: ", request.session.get('eliminadas')
    
        return render_to_response('jogo/partida.html', {'confs': request.session['confs'], 'pergunta' : pergunta, 'alternativas' : mixed, 'respondidas' : request.session.get('respondidas'), 'ajudas' : request.session.get('ajudas'), 'eliminadas' : request.session.get('eliminadas')}, context_instance=RequestContext(request))
    # Usuário ainda não configurou a partida
    else:
        return HttpResponse("Vc ainda nao configurou sua partida.")

def config(request):
    # Mock para as opções do usuário
    dificuldade = 2
    temas = ['Cinema', 'Televisão']
    # Cria um novo objeto passando as opções do usuário
    conf = Partidaconfs(dificuldade, temas)
    # Coloca na sessão
    request.session.clear()
    request.session['confs'] = conf
    
    # Inicializa as ajudas. Só um mock por enquanto
    ajudas = {'troca' : 3, 'elimina' : 3, 'tempo' : 3}
    request.session['ajudas'] = ajudas
    
    return render_to_response('jogo/config.html')

def responder(request):
    """
    Vem para cá quando o usuário responde uma pergunta.
    O request deve conter a resposta dada pelo usuário e o id da pergunta.
    """
    altSelecionada = request.POST["alternativa"]
    
    if 'respondidas' not in request.session:
        request.session['respondidas'] = 0
    
    if 'pergunta' in request.session:
        pergunta = request.session['pergunta']
        
        # Retira a pergunta da sessão. Necessário pois a view Partida só carrega uma pergunta nova se não houver nenhuma na sessão.
        del request.session['pergunta'] 
        
        # Retira a lista de eliminadas tb (importante caso 2 perguntas tenham alternativas iguais)
        del request.session['eliminadas']
        
        if pergunta.altCorreta == altSelecionada:
            if int(request.session['respondidas']) == 4:
                # Respondeu a ultima pergunta corretamente. Fim de jogo.
                return HttpResponseRedirect(reverse('osindicados.jogo.views.ganhou'))
            else:
                # Respondeu certo, mas nao eh a ultima
                request.session['respondidas'] = int(request.session['respondidas']) + 1
                return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
        else:
            #Respondeu errado. Fim de jogo.
            request.session.clear()
            return HttpResponseRedirect(reverse('osindicados.jogo.views.erro'))
    

def erro(request):
    return render_to_response('jogo/erro.html')

def ganhou(request):
    return render_to_response('jogo/ganhou.html')

def ajudaTroca(request):
    # Verifica se o usuário tem mesmo uma ajuda de troca.
    ajudas = request.session['ajudas']
    trocas = int(ajudas['troca'])
    if trocas > 0:
        # Diminui uma ajuda de troca
        ajudas['troca'] = trocas - 1
        request.session['ajudas'] = ajudas
        # Retira a pergunta da sessão, para poder trocar
        del request.session['pergunta']
        # Retira a lista de eliminadas tb (importante caso 2 perguntas tenham alternativas iguais)
        del request.session['eliminadas']
        # Volta à tela de partida
        return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
    # Não tinha uma ajuda.
    else:
        return HttpResponse("Voce est&aacute; roubando...")
    
def ajudaElimina(request):
    
    print "Entrooou"
    
    # Verifica se o usuário tem mesmo uma ajuda de eliminação
    ajudas = request.session['ajudas']
    eliminacoes = int(ajudas['elimina'])
    
    if eliminacoes > 0:        
        # Recupera a pergunta e as alternativas (na ordem em que elas estão na tela)
        alternativas = request.session['alternativas']
        pergunta = request.session['pergunta']
        
        # Só pega as erradas, embaralha, retira as duas primeiras e marca como eliminadas (põe na sessão)
        alternativasErradas = [alt for alt in alternativas if alt != pergunta.altCorreta]
        random.shuffle(alternativasErradas)
        eliminadas = alternativasErradas[2:4]
        request.session['eliminadas'] = eliminadas
        
        print eliminadas
        
        # Diminui uma ajuda de eliminação
        ajudas['elimina'] = eliminacoes - 1
        request.session['ajudas'] = ajudas
        
        # Volta para a partida
        return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
    else:
        return HttpResponse('Voce esta roubando...')
        
    
    
    