# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^jogo/', include('osindicados.jogo.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^$', include(admin.site.urls)),
                       )

        