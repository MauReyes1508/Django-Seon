from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register_user'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu_rutinas/', views.menu_rutinas, name='menu_rutinas'),
    path('registro_terceros/', views.registro_terceros, name='registro_terceros'),
    path('lista_terceros/', views.lista_terceros, name='lista_terceros'),
    path('actualizar_tercero', views.actualizar_tercero, name='actualizar_tercero'),
]

