# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
import os.path

urlpatterns = patterns('',
  (r'^$', 'osindicados.backup.views.index'),
  (r'^backup_data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.ROOT_PATH, "backup", "backup_data")}),
)