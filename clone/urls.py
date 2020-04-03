from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from clone import views 


urlpatterns  = [
    url('^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='create-profile'),
    url(r'^profile/(\d+)/$', views.profile_user, name='dipslay-profile'),
    url(r'^post/image/', views.uploadimage, name = 'uploadimage'),
    url(r'^search/', views.search, name='searchbyusername'),
    url(r'^comment/(?P<id>\d+)/$', views.comment, name='comment'),
    url(r'^image/(?P<img_id>\d+)/$', views.specific, name='single-image'),
    url(r'^likes/(?P<img_id>\d+)/$', views.likes, name='likes'),
    # url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        # url(r'^logout/$', views.logout_view, name='logout'),
