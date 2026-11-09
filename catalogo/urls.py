from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home, name="home"),
    path("busca/", views.busca, name="busca"),
    path("categoria/<int:pk>/", views.categoria_detail, name="categoria_detail"),
    path("artigo/<int:pk>/", views.artigo_detail, name="artigo_detail"),
]
