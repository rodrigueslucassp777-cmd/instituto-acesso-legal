from django.contrib import admin

from .models import Artigo, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "data_atualizacao")
    list_filter = ("categoria",)
    search_fields = ("titulo", "palavras_chave", "conteudo_simplificado")
    autocomplete_fields = ("categoria",)
    readonly_fields = ("data_atualizacao",)
