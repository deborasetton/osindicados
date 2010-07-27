# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from osindicados.jogo.models import DIFICULDADES, Tema, Pergunta, \
    Placar
from osindicados.jogo.partidaconfs import *
from osindicados.jogo.utils import sortearAlternativas, selectPlacares
import time
import random



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
        return render_to_response('jogo/partida.html', {'confs': request.session['confs'], 'pergunta' : request.session['pergunta'], 'alternativas' : request.session.get('alternativas'), 'respondidas' : request.session.get('respondidas'), 'ajudas' : request.session.get('ajudas'), 'eliminadas' : request.session.get('eliminadas'), 'placar' : request.session.get('placar')}, context_instance=RequestContext(request))

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

        return render_to_response('jogo/partida.html', {'confs': request.session['confs'], 'pergunta' : pergunta, 'alternativas' : mixed, 'respondidas' : request.session.get('respondidas'), 'ajudas' : request.session.get('ajudas'), 'eliminadas' : request.session.get('eliminadas'), 'placar' : request.session.get('placar')}, context_instance=RequestContext(request))
    # Usuário ainda não configurou a partida
    else:
        return HttpResponse("Vc ainda nao configurou sua partida.")

def config(request):
    """
    Configurações do jogo, é a tela inicial do sistema inteiro
    O request deve conter o tema e a dificuldade
    """
    if 'tema' and 'dificuldade' in request.POST:
        # Cria um novo objeto passando as opções do usuário
        conf = Partidaconfs(request.POST['dificuldade'], request.POST.getlist('temas'))

        # Coloca na sessão
        request.session.clear()
        request.session['confs'] = conf

        # Inicializa as ajudas de acordo com a dificuldade
        # são três para o nível amador(1), duas para profissional(2), uma para celebridade(3) e nenhuma vez para ídolo(4)
        numajudas = 3 #amador
        if request.POST['dificuldade'] == '4':
            numajudas = 0 # ídolo
        if request.POST['dificuldade'] == '3':
            numajudas = 1 # celebridade
        if request.POST['dificuldade'] == '2':
            numajudas = 2 # profissional
        ajudas = {'troca' : numajudas, 'elimina' : numajudas, 'tempo' : numajudas}
        request.session['ajudas'] = ajudas

        # Inicializa Placar()
        placar = Placar()
        request.session['placar'] = placar

        return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
    else:
        return render_to_response('jogo/config.html', {'dificuldades': DIFICULDADES, 'temas' : Tema.objects.all() }, context_instance=RequestContext(request))

def responder(request):
    """
    Executado quando o usuário responde uma pergunta.
    O request deve conter a resposta dada pelo usuário e o id da pergunta.
    """
    # Verificacao de tempo
    horarioInicio = float(request.session['hr_inicio']) # Horario em que o timer foi iniciado
    horarioFim = float(request.POST['hr']) # Horario em que o form foi submetido

    if 'hr_extensao' in request.session:
        # Se houve extensao, o usuario teve 60 segundos para responder
        horarioFimTeorico = horarioInicio + 60
        del request.session['hr_extensao']
        del request.session['hr_inicio']
    else:
        # Se nao houve extensao, o usuario teve so 30 segundos para responder
        horarioFimTeorico = horarioInicio + 30

    # Informacao de debug
    print (horarioFim - horarioInicio)
    print (horarioFim - horarioFimTeorico)

    # Tolerancia maxima de 1 segundo de diferenca entre o esperado e o real
    if (horarioFim - horarioFimTeorico) > 1:
        request.session.clear()
        return HttpResponseRedirect(reverse('osindicados.jogo.views.erro'))

    # Passou pela verificacao de tempo. Comeca a logica da resposta.

    altSelecionada = request.POST["alternativa"]

    if 'respondidas' not in request.session:
        request.session['respondidas'] = 0

    if 'pergunta' in request.session:
        pergunta = request.session['pergunta']

        # Retira a pergunta da sessão. Necessário pois a view Partida só carrega uma pergunta nova se não houver nenhuma na sessão.
        del request.session['pergunta']

        # Retira a lista de eliminadas tb (importante caso 2 perguntas tenham alternativas iguais)
        if 'eliminadas' in request.session:
            del request.session['eliminadas']

        if pergunta.altCorreta == altSelecionada:
            if int(request.session['respondidas']) == 4:
                # Respondeu a ultima pergunta corretamente. Fim de jogo.
                # Atualiza o placar antes.
                request.session['placar'] = incrementarPlacar(request.session['placar'], pergunta)
                return HttpResponseRedirect(reverse('osindicados.jogo.views.ganhou'))
            else:
                # Respondeu certo, mas nao eh a ultima
                # Atualiza o placar
                request.session['placar'] = incrementarPlacar(request.session['placar'], pergunta)
                # Atualiza o numero de perguntas respondidas
                request.session['respondidas'] = int(request.session['respondidas']) + 1
                return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
        else:
            #Respondeu errado. Fim de jogo.
            request.session.clear()
            return HttpResponseRedirect(reverse('osindicados.jogo.views.erro'))


def erro(request):
    """
    Executado quando o usuário erra uma pergunta, quando o tempo esgota ou quando se verifica que o usuário
    está trapaceando (por exemplo, alterar o timer da tela).
    """
    return render_to_response('jogo/erro.html')

def ganhou(request):
    """
    Executado quando o usuário ganha a partida (25 respostas corretas)
    """
    return render_to_response('jogo/ganhou.html', context_instance=RequestContext(request))

def ajudaTroca(request):
    """
    Executado quando o usuário solicita a ajuda de troca de pergunta.
    Verifica se o usuário ainda pode solicitar esta ajuda e, caso possa, retira da sessão a pergunta atual e
    redireciona à tela de partida
    """
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
        if 'eliminadas' in request.session:
            del request.session['eliminadas']
        # Volta à tela de partida
        return HttpResponseRedirect(reverse('osindicados.jogo.views.partida'))
    # Não tinha uma ajuda.
    else:
        return HttpResponse("Voce est&aacute; roubando...")

def ajudaElimina(request):
    """
    Executado quando o usuário solicita uma ajuda de eliminação de alternativas.
    Verifica se o usuário ainda pode solicitar esta ajuda e, caso possa, embaralha as alternativas erradas
    e marca as duas primeiras como eliminadas.
    """
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

def horario(request):
    """
    Executado quando o timer da tela de pergunta é iniciado. Retorna o horário atual do servidor, para sincronia
    com o browser do cliente, e grava na sessão o horário de início da contagem.
    """
    now = time.time()
    request.session['hr_inicio'] = now
    return HttpResponse(now)

def ajudaTempo(request):
    """
    Executado quando o usuário solicita uma ajuda de extensão de tempo.
    Apenas grava o horário que o usuário solicitou a ajuda, para conferir mais tarde se o tempo
    de resposta não passou de 60 segundos.
    """

    # Verifica se o usuário tem mesmo uma ajuda de tempo
    ajudas = request.session['ajudas']
    ajudasTempo = int(ajudas['tempo'])

    if ajudasTempo > 0:
        now = time.time()
        request.session['hr_extensao'] = now
        return HttpResponse(now)
    else:
        return HttpResponse('Voce esta roubando...')

def entrarRanking(request):
    """
    Executado quando o usuário submete o form de entrar para o ranking.
    Pensar se não dá para colocar tudo no método ranking mesmo.
    """

    # Nome do usuário
    nomeUsuario = request.POST['nomeUsuario']
    # Placar do usuário
    placarUsuario = request.session['placar']
    # Configurações da partida (dificuldade e temas)
    configuracoesPartida = request.session['confs']

    # Atualiza o placar com o nome do jogador
    placarUsuario.nomeJogador = nomeUsuario
    # Atualiza o placar com a dificuldade da partida
    placarUsuario.dificuldade = int(configuracoesPartida.dificuldade)

    # Para debug, tirar depois
    print placarUsuario.nomeJogador
    print placarUsuario.dificuldade
    print placarUsuario

    # Salva o placar no BD
    placarUsuario.save()

    # Redireciona à tela de ranking
    return HttpResponseRedirect(reverse('osindicados.jogo.views.ranking'))

def ranking(request):
    temas = Tema.objects.all()

    #Se o usuário configurou uma partida exibe o ranking pelos temas
    if 'confs' in request.session:

        # Se o usuário está solicitando uma filtragem de dados substitui os temas
        if request.method=='POST':
            request.session['confs'].temas=request.POST.getlist('temasSelecionados')

        return render_to_response('jogo/ranking.html', {'placares' : selectPlacares(request.session['confs'].temas), 'temas' : temas}, context_instance=RequestContext(request))

    #Caso o usuário não tenha configurado uma partida exibe o ranking geral
    else:
        listaDeTemas = []
        for t in temas:
            listaDeTemas.append(t.nome)
        return render_to_response('jogo/ranking.html', {'placares' : selectPlacares(listaDeTemas), 'temas' : temas}, context_instance=RequestContext(request))

def testedesign(request):
    return render_to_response('jogo/testedesign.html')

########################### Funções auxiliares ##############################

def incrementarPlacar(placar, pergunta):
    """
    Incrementa o placar atual do jogador, de acordo com o tema da pergunta que foi acertada.
    TODO: Apagar os prints, são apenas para debug
    """
    print 'Entrou ', pergunta.idAssunto.nome, placar

    if(pergunta.idAssunto.nome == 'Esporte'):
        print 'Esporte!'
        placar.acertosEsporte = int(placar.acertosEsporte) + 1
    elif(pergunta.idAssunto.nome == 'Conhecimentos Gerais'):
        print 'CG!'
        placar.acertosCGerais = int(placar.acertosCGerais) + 1
    elif(pergunta.idAssunto.nome == 'Cinema'):
        print 'Cinema!'
        placar.acertosCinema = int(placar.acertosCinema) + 1
    elif(pergunta.idAssunto.nome == u'Televis\xe3o'):
        print 'TV!'
        placar.acertosTelevisao = int(placar.acertosTelevisao) + 1
    elif(pergunta.idAssunto.nome == u'Ci\xeancias'):
        print 'Ciencias!'
        placar.acertosCiencias = int(placar.acertosCiencias) + 1
    elif(pergunta.idAssunto.nome == u'M\xfasica'):
        print 'Musica!'
        placar.acertosMusica = int(placar.acertosMusica) + 1
    print 'Saiu ', placar
    return placar

