"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reservations',views.viewsets_reservation)
from tickets.views import no_rest_no_model
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('django/jsonresponsemodel/', views.no_rest_no_model),
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),
    path('rest/FBV_LIST/', views.FBV_LIST),
    path('rest/fbv/<int:pk>', views.FBV_PK ),
    path('rest/cbv/', views.CBV_LIST.as_view() ),
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view() ),
    path('rest/mixins/', views.Mixins_list.as_view() ),
    path('rest/mixins/<int:pk>', views.Mixins_pk.as_view() ),
    path('rest/generics/', views.generics_list.as_view() ),
    path('rest/generics/<int:pk>', views.generics_pk.as_view() ),
    path('rest/viewset/',include(router.urls)),
    path('fbv/findmovie',views.find_movie),
    path('fbv/newreservation',views.new_reservation),
    path('api-auth',include('rest_framework.urls')),
    path('api-token-auth',obtain_auth_token),
    path('post/generics/<int:pk>', views.Post_pk.as_view() ),

    
]
