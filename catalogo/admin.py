from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Artigo, Categoria


@admin.register(Categoria)
class CategoriaAdmin(SimpleHistoryAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)
    history_list_display = ("nome", "descricao", "icone_url")


@admin.register(Artigo)
class ArtigoAdmin(SimpleHistoryAdmin):
    list_display = ("titulo", "categoria", "data_atualizacao")
    list_filter = ("categoria",)
    search_fields = ("titulo", "palavras_chave", "conteudo_simplificado")
    autocomplete_fields = ("categoria",)
    readonly_fields = ("data_atualizacao",)
    history_list_display = ("titulo", "categoria", "conteudo_simplificado")
