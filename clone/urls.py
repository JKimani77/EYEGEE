from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from clone import views 


urlpatterns  = [
    url('^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='create-profile'),
    url(r'^profile/<int:id>$', views.profile_user, name='dipslay-profile'),
    url(r'^post/image/$', views.uploadimage, name = 'uploadimage'),
    url(r'^search/$', views.search, name='searchbyusername'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)