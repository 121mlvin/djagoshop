from django.contrib import admin
from django.urls import path, include
from goodsapp.views import *



urlpatterns = [
    path('', include('goodsapp.urls')),
    path('', include('coreapp.urls')),
    path('account/', include('allauth.urls')),
    path('admin/', admin.site.urls),

]
