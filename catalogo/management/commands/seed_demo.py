from django.core.management.base import BaseCommand

from catalogo.models import Artigo, Categoria


class Command(BaseCommand):
    help = "Popula o banco com categorias e artigos de exemplo para desenvolvimento."

    def handle(self, *args, **options):
        trabalho, _ = Categoria.objects.get_or_create(
            nome="Trabalho",
            defaults={
                "descricao": "Direitos relacionados ao emprego e à carteira de trabalho.",
                "icone_url": "fa-solid fa-briefcase",
            },
        )
        moradia, _ = Categoria.objects.get_or_create(
            nome="Moradia",
            defaults={
                "descricao": "Direitos de quem aluga ou mora de favor.",
                "icone_url": "fa-solid fa-house",
            },
        )

        Artigo.objects.get_or_create(
            titulo="Direito a férias remuneradas",
            defaults={
                "categoria": trabalho,
                "conteudo_simplificado": (
                    "Todo trabalhador com carteira assinada tem direito a 30 dias de "
                    "férias remuneradas após completar 12 meses de trabalho (período "
                    "aquisitivo). O pagamento das férias deve ser feito até 2 dias "
                    "antes do início do descanso, com acréscimo de 1/3 do salário."
                ),
                "palavras_chave": "férias, descanso, carteira assinada, CLT, 1/3 constitucional",
            },
        )
        Artigo.objects.get_or_create(
            titulo="Devolução do depósito de aluguel",
            defaults={
                "categoria": moradia,
                "conteudo_simplificado": (
                    "Ao final do contrato de aluguel, se o imóvel for devolvido em "
                    "boas condições, o proprietário deve devolver o valor do depósito "
                    "(caução) pago no início, descontando apenas danos comprovados."
                ),
                "palavras_chave": "aluguel, caução, depósito, locação, contrato",
            },
        )

        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados com sucesso."))
