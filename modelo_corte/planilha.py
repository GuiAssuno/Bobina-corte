from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, PatternFill, Font
from tkinter import filedialog
import pandas as pd
import io

class excel:
    def __init__ (self, cortes, padroes, perdas, p_escolhidos):
        self.cortes = cortes
        self.padroes = padroes
        self.perdas = perdas
        self.p_escolhidos = [x for x in p_escolhidos.iloc[:, 0]]
        self.buffer = io.BytesIO()

        self.tipos_excel = [
            ("Pasta de Trabalho do Excel", "*.xlsx"),
            ("Pasta de Trabalho Habilitada para Macro", "*.xlsm"),
            ("Pasta de Trabalho Binária do Excel", "*.xlsb"),
            ("Pasta de Trabalho do Excel 97-2003", "*.xls"),
            ("Arquivo CSV (separado por vírgulas)", "*.csv"),
            ("Texto separado por tabulações", "*.txt"),
            ("Todos os arquivos", "*.*")
        ]

        # Cria uma nova pasta de trabalho (Workbook)
        self.wb = Workbook()

        # Seleciona a aba ativa
        self.ws = self.wb.active
        self.ws.title = "Padrões"

        # Cabeçalho formatado
        self.cabecalho = Font(bold=True, color="FFFFFFFF")

        # Mudando a cor de fundo
        # A cor deve ser passada em formato hexadecimal ARGB. Ex: Amarelo = "FFFF00"
        self.cor_fundo_descartado = PatternFill(start_color="FFEEEEEE", end_color="FFEEEEEE", fill_type="solid") # Cinza claro
        self.cor_fundo_usado = PatternFill(start_color="F295D0A1", end_color="F295D0A1", fill_type="solid") # Verde acizentado
        self.cor_fundo_header = PatternFill(start_color="FF2E2E2E", end_color="FF2E2E2E", fill_type="solid") # Cinza escuro

        # Centralizando o conteúdo
        self.alinhamento = Alignment(horizontal="center", vertical="center")

        # Colocando borda
        # Primeiro definimos o estilo da linha (fina e preta), depois aplicamos aos 4 lados da célula
        self.linha_fina = Side(border_style="thin", color="FF000000")

        self.borda_fina = Border(left=self.linha_fina, right=self.linha_fina, top=self.linha_fina, bottom=self.linha_fina)
        # Borde Style:
        # • thin (fina)
        # • medium (média)
        # • thick (grossa)
        # • double (dupla)
        # • dotted (pontilhada)
        # • dashed (tracejada)
        # • hair (cabelo / linha extremamente fina)
        # • mediumDashed (média tracejada)
        # • dashDot (traço-ponto)
        # • mediumDashDot (média traço-ponto)
        # • dashDotDot (traço-ponto-ponto)
        # • mediumDashDotDot (média traço-ponto-ponto)
        # • slantDashDot (traço-ponto inclinado)

    def criar_cabecalho(self):
        # Adicionar cabeçalho
        self.ws["A1"] = "ID"

        for i, c in enumerate(self.cortes, 2):
            nm_col = f"{c} cm"
            self.ws.cell(row=1, column=i, value=nm_col)

        coluna_perdas = len(self.cortes)+2

        self.ws.cell(row=1, column=coluna_perdas, value="Perda (cm)")

        letra = list("AABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Alenta um pouco a largura da celula
        self.ws.column_dimensions[letra[coluna_perdas]].width = 17

    def adicionar_dados(self):
        # Adiciona dados nas linhas
        for id, x in enumerate(zip(self.padroes, self.perdas)): 
            self.ws.append([id+1, *x[0], x[1]])

    def obter_caminho(self, nome):
        caminho = filedialog.asksaveasfilename(
            initialfile = nome,
            defaultextension=".xlsx", 
            filetypes = self.tipos_excel,
            title="Salvar Padrões"
            )

        # return caminho

    def salvar_arquivo(self, arquivo):
        self.criar_cabecalho()
        self.adicionar_dados()
        print(self.p_escolhidos)
        for linha in self.ws.iter_cols(min_row=1, max_row=self.ws.max_row, min_col=1, max_col=self.ws.max_column):
            for x, celula in enumerate(linha):
                
                if not x: # Cabeçalho
                    celula.fill = self.cor_fundo_header
                    celula.alignment = self.alinhamento
                    celula.border = self.borda_fina
                    celula.font = self.cabecalho
                else: 
                    if x in self.p_escolhidos: # Padroes usados
                        celula.fill = self.cor_fundo_usado
                        celula.alignment = self.alinhamento
                        celula.border = self.borda_fina
                    else: # Padroes não usados
                        celula.fill = self.cor_fundo_descartado
                        celula.alignment = self.alinhamento
                        celula.border = self.borda_fina

        # Escolhe o caminho que quer salvar 
        #caminho_salvar = self.obter_caminho(f"{arquivo}_padroes calculados")
        # buffer = io.BytesIO()
        # Salva o arquivo Excel
        self.wb.save(self.buffer)
        self.buffer.seek(0)