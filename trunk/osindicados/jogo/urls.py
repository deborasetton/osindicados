# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns

urlpatterns = patterns('osindicados.jogo.views',
  (r'^$', 'index'),
  (r'^partida/$', 'partida'),
  (r'^config/$', 'config'),
  (r'^responder/$', 'responder'),
  (r'^erro/$', 'erro'),
  (r'^ganhou/$', 'ganhou'),
  (r'^ajudaTroca/$', 'ajudaTroca'),
  (r'^ajudaElimina/$', 'ajudaElimina'),
  (r'^ajudaTempo/$', 'ajudaTempo'),
  (r'^horario/$', 'horario'),
  (r'^entrarRanking/$', 'entrarRanking'),
  (r'^ranking/$', 'ranking'),
  (r'^design/$', 'testedesign'),
)