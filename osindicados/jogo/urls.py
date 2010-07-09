# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from osindicados.jogo.models import Tema
from osindicados.jogo.models import Pergunta

urlpatterns = patterns('osindicados.jogo.views',
	(r'^$', 'index')
)