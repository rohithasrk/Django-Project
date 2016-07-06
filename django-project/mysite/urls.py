from django.conf.urls import url,include
from django.contrib import admin

from . import index

urlpatterns = [
    url(r'^$', index.tem ,name='tem'),
    url(r'^admin/', admin.site.urls),
    url(r'^polls/',include('polls.urls')),
]
