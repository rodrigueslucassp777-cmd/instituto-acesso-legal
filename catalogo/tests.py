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

    def test_lista_temas_em_destaque(self):
        categoria = Categoria.objects.create(nome="Consumidor")
        artigo = Artigo.objects.create(
            categoria=categoria,
            titulo="Garantia estendida",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="garantia, produto",
        )
        response = self.client.get(reverse("catalogo:home"))
        self.assertContains(response, artigo.titulo)


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

    def test_mostra_artigos_relacionados_da_mesma_categoria(self):
        relacionado = Artigo.objects.create(
            categoria=self.categoria,
            titulo="Troca por defeito",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="troca, defeito",
        )
        response = self.client.get(
            reverse("catalogo:artigo_detail", args=[self.artigo.pk])
        )
        self.assertContains(response, relacionado.titulo)

    def test_nao_mostra_artigos_de_outra_categoria_como_relacionados(self):
        outra_categoria = Categoria.objects.create(nome="Moradia")
        nao_relacionado = Artigo.objects.create(
            categoria=outra_categoria,
            titulo="Despejo",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="despejo, aluguel",
        )
        response = self.client.get(
            reverse("catalogo:artigo_detail", args=[self.artigo.pk])
        )
        self.assertNotContains(response, nao_relacionado.titulo)


class AuditoriaHistoricoTests(TestCase):
    def test_edicao_de_artigo_gera_registro_no_historico(self):
        categoria = Categoria.objects.create(nome="Trabalho")
        artigo = Artigo.objects.create(
            categoria=categoria,
            titulo="Hora extra",
            conteudo_simplificado="Conteúdo de exemplo.",
            palavras_chave="hora extra, trabalho",
        )
        artigo.titulo = "Hora extra remunerada"
        artigo.save()

        self.assertEqual(artigo.history.count(), 2)
        self.assertEqual(artigo.history.earliest().titulo, "Hora extra")
        self.assertEqual(artigo.history.latest().titulo, "Hora extra remunerada")


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
