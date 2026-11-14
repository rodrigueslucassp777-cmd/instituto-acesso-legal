from django.test import TestCase
from django.urls import reverse

from .models import Artigo, Categoria


class CategoriaModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Trabalho", descricao="Direitos trabalhistas")

    def test_str_retorna_nome(self):
        self.assertEqual(str(self.categoria), "Trabalho")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.categoria.get_absolute_url(),
            reverse("catalogo:categoria_detail", args=[self.categoria.pk]),
        )


class ArtigoModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Moradia")
        self.artigo = Artigo.objects.create(
            categoria=self.categoria,
            titulo="Direito à moradia",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="moradia, aluguel, despejo",
        )

    def test_str_retorna_titulo(self):
        self.assertEqual(str(self.artigo), "Direito à moradia")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.artigo.get_absolute_url(),
            reverse("catalogo:artigo_detail", args=[self.artigo.pk]),
        )


class HomeViewTests(TestCase):
    def test_lista_categorias(self):
        categoria = Categoria.objects.create(nome="Saúde")
        response = self.client.get(reverse("catalogo:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, categoria.nome)


class CategoriaDetailViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Educação")

    def test_categoria_existente_retorna_200(self):
        response = self.client.get(
            reverse("catalogo:categoria_detail", args=[self.categoria.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_categoria_inexistente_retorna_404(self):
        response = self.client.get(
            reverse("catalogo:categoria_detail", args=[self.categoria.pk + 999])
        )
        self.assertEqual(response.status_code, 404)


class ArtigoDetailViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Consumidor")
        self.artigo = Artigo.objects.create(
            categoria=self.categoria,
            titulo="Garantia de produtos",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="garantia, produto, defeito",
        )

    def test_artigo_existente_retorna_200(self):
        response = self.client.get(
            reverse("catalogo:artigo_detail", args=[self.artigo.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_artigo_inexistente_retorna_404(self):
        response = self.client.get(
            reverse("catalogo:artigo_detail", args=[self.artigo.pk + 999])
        )
        self.assertEqual(response.status_code, 404)


class BuscaViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Trabalho")
        self.artigo = Artigo.objects.create(
            categoria=self.categoria,
            titulo="Férias remuneradas",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="férias, descanso, remuneração",
        )

    def test_busca_direta_encontra_artigo(self):
        response = self.client.get(reverse("catalogo:busca"), {"q": "Férias"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artigo.titulo)

    def test_busca_tolerante_a_acentos(self):
        response = self.client.get(reverse("catalogo:busca"), {"q": "ferias"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artigo.titulo)

    def test_busca_sem_resultados(self):
        response = self.client.get(reverse("catalogo:busca"), {"q": "inexistente"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.artigo.titulo)
