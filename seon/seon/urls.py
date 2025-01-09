from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.registro_terceros, name='registro_terceros'),
    path('lista_terceros/', views.lista_terceros, name='lista_terceros'),
    path('actualizar_tercero', views.actualizar_tercero, name='actualizar_tercero'),
]

