from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from unidecode import unidecode

from .models import Artigo, Categoria


def _normalizar(texto):
    """Remove acentos e caixa para comparação tolerante a erros de digitação."""
    return unidecode(texto or "").lower()


def home(request):
    categorias = Categoria.objects.all()
    return render(request, "catalogo/home.html", {"categorias": categorias})


def busca(request):
    termo = request.GET.get("q", "").strip()
    resultados = []

    if termo:
        termo_normalizado = _normalizar(termo)

        # 1ª tentativa: filtro direto no banco (case-insensitive) via Q objects.
        candidatos = Artigo.objects.select_related("categoria").filter(
            Q(titulo__icontains=termo) | Q(palavras_chave__icontains=termo)
        )

        # Se o usuário digitou sem os acentos corretos, cai para comparação
        # tolerante a acentos em memória (catálogo é pequeno, custo é aceitável).
        if not candidatos.exists():
            candidatos = Artigo.objects.select_related("categoria").all()
            resultados = [
                artigo
                for artigo in candidatos
                if termo_normalizado in _normalizar(artigo.titulo)
                or termo_normalizado in _normalizar(artigo.palavras_chave)
            ]
        else:
            resultados = list(candidatos)

    return render(
        request,
        "catalogo/busca.html",
        {"termo": termo, "resultados": resultados},
    )


def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    artigos = categoria.artigos.all()
    return render(
        request,
        "catalogo/categoria_detail.html",
        {"categoria": categoria, "artigos": artigos},
    )


def artigo_detail(request, pk):
    artigo = get_object_or_404(Artigo.objects.select_related("categoria"), pk=pk)
    return render(request, "catalogo/artigo_detail.html", {"artigo": artigo})
