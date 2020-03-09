from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 


urlpatterns  = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='create-profile'),
    path('profile/<int:id>', views.profile_user, name='dipslay-profile'),
    path('post/image', views.uploadimage, name = 'uploadimage'),
    path('search/', views.search, name='search-user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)