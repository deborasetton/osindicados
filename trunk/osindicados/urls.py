# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^jogo/', include('osindicados.jogo.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^osindicadosmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^$', include(admin.site.urls)),
                       )

        