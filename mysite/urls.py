from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^articles/', include('articles.urls',
                               namespace='articles',
                               app_name='articles')),
    url(r'^admin/', admin.site.urls),
]
