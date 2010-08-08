from django import template
from osindicados.jogo.models import Tema
from osindicados.jogo.views import temasjogo
from ctypes.wintypes import INT


register = template.Library()

@register.filter
def faltam(value):
    """
    Recebe o valor de perguntas ja respondidas e retorna
    a quantidade de perguntas que faltam para finalizar 
    a partida. Por enquanto, sao 5 perguntas para terminar.
    """
    return (5 - int(value))

@register.filter
def imprimirEstrelas(value):
    """
    aaa
    """
    
    imgUsedHTML = "<img src='/osindicadosmedia/img/starblack.png'/>"
    imgLeftHTML = "<img src='/osindicadosmedia/img/star.png'/>"
    resultado = ""
    
    starsLeft = int(value)
    starsUsed = 3 - starsLeft

    print "Leaaaaaaaaaaaaaaft:", starsLeft
    print "Used:", starsUsed
    
    for i in range(starsUsed):
        resultado += imgUsedHTML
    for i in range(starsLeft):
        resultado += imgLeftHTML
    
    print resultado
    return resultado

@register.filter
def imprimirPlacar(placar, temas):
    """
    aaa
    """
    
    imgHTML = "<img src='/osindicadosmedia/img/star.png'/>"
    resposta = ""
    print placar
    print temas
    
    for tema in temas:
        chave = getPlacarKey(tema)
        ponto = placar.get(chave)
        
    resultado = "haa"
    return resultado

def getPlacarKey(tema):
    if(tema == 'Esporte'):
        return 'Esporte'
    elif(tema == 'Conhecimentos Gerais'):
        return 'CGerais!'
    elif(tema == 'Cinema'):
        return 'Cinema!'
    elif(tema == u'Televis\xe3o'):
        return 'Televisao'
    elif(tema == u'Ci\xeancias'):
        return 'Ciencias!'
    elif(tema == u'M\xfasica'):
        return 'Musica!'   
    
@register.filter
def getPontos(tema, placar):
    """
    aaa
    """
    print tema
    print placar
    
    #p = Placar(placar)
    #print "p: ", p
    #print "pcinema: ", p['Cinema']
    
#    if isinstance(placar, tuple):
#        print "Tuple"
#    elif isinstance(placar, dict):
#        print "Dict"
#    elif isinstance(placar, basestring):
#        print 'Str'
#    else:
#        print "nada"
#        
#    print "tipo"
#    print type(placar)
#    
#    q = placar
#    print "qcinema: ", q['Cinema']
    
    if(tema == 'Esporte'):
        return placar.acertosEsporte
    elif(tema == 'Conhecimentos Gerais'):
        return placar.acertosCGerais
    elif(tema == 'Cinema'):
        return placar.acertosCinema
    elif(tema == u'Televis\xe3o'):
        return placar.acertosTelevisao
    elif(tema == u'Ci\xeancias'):
        return placar.acertosCiencias
    elif(tema == u'M\xfasica'):
        return placar.acertosMusica
    
@register.filter
def printTema(tema, placar):
    """
    aaa
    """
    
    if(tema == 'Esporte'):
        nomeTema = 'Esporte'
        acertos = placar.acertosEsporte
        imagem = "vuvuzelaouro.png"
    elif(tema == 'Conhecimentos Gerais'):
        nomeTema = 'Conhecimentos Gerais'
        acertos = placar.acertosCGerais
        imagem = "diploma.png"
    elif(tema == 'Cinema'):
        nomeTema = 'Cinema'
        acertos = placar.acertosCinema
        imagem = "oscar.png"
    elif(tema == u'Televis\xe3o'):
        nomeTema = u'Televis\xe3o'
        acertos = placar.acertosTelevisao
        imagem = "emmy.png"
    elif(tema == u'Ci\xeancias'):
        nomeTema = u'Ci\xeancias'
        acertos = placar.acertosCiencias
        imagem = "nobel.png"
    elif(tema == u'M\xfasica'):
        nomeTema = u'M\xfasica'
        acertos = placar.acertosMusica
        imagem = "grammy.png"
    
    resultado = "<p style=\"text-align: center; margin:0px; padding: 0px\"><img src='/osindicadosmedia/img/" + imagem + "' width=\"\" height=\"30px\" title='Pontos de " + nomeTema + "' alt='Pontos de " + nomeTema + "' />" + "<br/>" +  str(acertos) + "</p><br/>"
    print resultado   
    return resultado   

@register.filter
def getImagem(tema):
    """
    ....
    """
    obj = Tema.objects.filter(id=tema)
    print obj[0]
    img = obj[0].imagemTrofeu
    nomeTema = obj[0].nome
    return "<img src='/osindicadosmedia/" + img + "' style=\"vertical-align: middle;\" title='" + nomeTema + "' alt='" + nomeTema + "' />"
       
@register.filter
def isInConfs(tema):
    """
    ....
    """
    
    temas = Tema.objects.all()
    nomes = [tema.nome for tema in temas]
    print "Tema:", tema
    print "Nomes:", nomes
    
    
    if(tema in nomes):
        return Tema.objects.filter(nome=tema)[0].imagemTrofeu
    else:
        return False;
   
@register.filter
def printVoceEstaAssistindo(temasSelecionados):
    """
    """
    print "Temas:"
    for tema in temasSelecionados:
        print tema
        
    print "TemasJogo:"    
    for temajogo in temasjogo:
        print temajogo
   
@register.filter
def nomeDificuldade(numeroDificuldade):
    """
    """
    print "Numero dificuldade:", numeroDificuldade
    numDificuldade = int(numeroDificuldade)
    
    if numDificuldade == 0:
        return "Amador"
    elif numDificuldade == 1:
        return "Profissional" 
    elif numDificuldade == 2:
        return "Celebridade"
    elif numDificuldade == 3:
        return "&Iacute;dolo"
    else:
        return "Desconhecida"   
    
    
    
    
    
    
    
    
      
