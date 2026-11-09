from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    icone_url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nome do ícone (ex.: Lucide 'scale' ou classe FontAwesome 'fa-scale-balanced').",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("catalogo:categoria_detail", args=[self.pk])


class Artigo(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="artigos"
    )
    titulo = models.CharField(max_length=200, unique=True)
    conteudo_simplificado = models.TextField()
    palavras_chave = models.TextField(
        help_text="Palavras separadas por vírgula, usadas pelo motor de busca."
    )
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ["-data_atualizacao"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("catalogo:artigo_detail", args=[self.pk])
