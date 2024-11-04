import json
import csv
import pickle
from functools import reduce


class Livro:
    def __init__(self, titulo, autor, ano_publicacao, genero):
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.genero = genero

    def __repr__(self):
        return f"Livro(titulo='{self.titulo}', autor='{self.autor}', ano_publicacao={self.ano_publicacao}, genero='{self.genero}')"


class Biblioteca:
    def __init__(self):
        self.lista_livros = []

    def adicionar_livro(self, livro):
        self.lista_livros.append(livro)

    def buscar_livros_por_autor(self, autor):
        return list(filter(lambda livro: livro.autor == autor, self.lista_livros))

    def salvar_para_texto(self, caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            for livro in self.lista_livros:
                arquivo.write(f"{livro.titulo}, {livro.autor}, {livro.ano_publicacao}, {livro.genero}\n")

    def carregar_de_texto(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                titulo, autor, ano_publicacao, genero = linha.strip().split(', ')
                self.adicionar_livro(Livro(titulo, autor, int(ano_publicacao), genero))

    def salvar_para_json(self, caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump([livro.__dict__ for livro in self.lista_livros], arquivo)

    def carregar_de_json(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            dados_livros = json.load(arquivo)
            for dados in dados_livros:
                self.adicionar_livro(Livro(**dados))

    def salvar_para_csv(self, caminho_arquivo):
        with open(caminho_arquivo, 'w', newline='') as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerow(['titulo', 'autor', 'ano_publicacao', 'genero'])
            for livro in self.lista_livros:
                escritor_csv.writerow([livro.titulo, livro.autor, livro.ano_publicacao, livro.genero])

    def carregar_de_csv(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                self.adicionar_livro(Livro(linha['titulo'], linha['autor'], int(linha['ano_publicacao']), linha['genero']))

    def salvar_para_binario(self, caminho_arquivo):
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.lista_livros, arquivo)

    def carregar_de_binario(self, caminho_arquivo):
        with open(caminho_arquivo, 'rb') as arquivo:
            self.lista_livros = pickle.load(arquivo)

    def listar_titulos(self):
        return list(map(lambda livro: livro.titulo, self.lista_livros))

    def contar_livros_por_genero(self, genero):
        return reduce(lambda total, livro: total + 1 if livro.genero == genero else total, self.lista_livros, 0)

    def filtrar_livros(self, ano_min=None, genero=None):
        return list(filter(lambda livro: 
                           (ano_min is None or livro.ano_publicacao >= ano_min) and 
                           (genero is None or livro.genero == genero), 
                           self.lista_livros))

    def fazer_backup(self, caminho_arquivo, formato='json'):
        if formato == 'json':
            self.salvar_para_json(caminho_arquivo)
        elif formato == 'binario':
            self.salvar_para_binario(caminho_arquivo)
        else:
            raise ValueError("Formato de backup inválido. Use 'json' ou 'binario'.")


# Exemplo de uso

biblioteca = Biblioteca()

# Adicionando livros
biblioteca.adicionar_livro(Livro("1984", "George Orwell", 1949, "Ficção"))
biblioteca.adicionar_livro(Livro("Orgulho e Preconceito", "Jane Austen", 1813, "Romance"))
biblioteca.adicionar_livro(Livro("O Senhor dos Anéis", "J.R.R. Tolkien", 1954, "Fantasia"))
biblioteca.adicionar_livro(Livro("Cem Anos de Solidão", "Gabriel Garcia Marquez", 1967, "Realismo Mágico"))
biblioteca.adicionar_livro(Livro("O Hobbit", "J.R.R. Tolkien", 1937, "Fantasia"))

# Consultar livros por autor
print("Livros de J.R.R. Tolkien:", biblioteca.buscar_livros_por_autor("J.R.R. Tolkien"))

# Contar livros por gênero
print("Total de livros de Fantasia:", biblioteca.contar_livros_por_genero("Fantasia"))

# Exportar e importar dados
biblioteca.salvar_para_texto("livros.txt")
biblioteca.salvar_para_json("livros.json")
biblioteca.salvar_para_csv("livros.csv")
biblioteca.salvar_para_binario("livros.bin")

# Testar importação
nova_biblioteca = Biblioteca()
nova_biblioteca.carregar_de_texto("livros.txt")
print("Importação de texto:", nova_biblioteca.lista_livros)

# Filtrar livros por ano e gênero
print("Livros após 1950 no gênero 'Fantasia':", biblioteca.filtrar_livros(ano_min=1950, genero="Fantasia"))

# Fazer backup
biblioteca.fazer_backup("backup.json", formato='json')
