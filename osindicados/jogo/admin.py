# -*- coding: utf-8 -*-
from django.contrib import admin
from osindicados.jogo.models import Pergunta
from osindicados.jogo.models import Tema

admin.site.register(Pergunta)
admin.site.register(Tema)
