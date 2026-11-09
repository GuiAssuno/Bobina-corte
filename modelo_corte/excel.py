from openpyxl import Workbook
from itertools import product
from openpyxl.styles import Border, Side, Alignment, PatternFill, Font
from tkinter import filedialog

tipos_excel = [
    ("Pasta de Trabalho do Excel", "*.xlsx"),
    ("Pasta de Trabalho Habilitada para Macro", "*.xlsm"),
    ("Pasta de Trabalho Binária do Excel", "*.xlsb"),
    ("Pasta de Trabalho do Excel 97-2003", "*.xls"),
    ("Arquivo CSV (separado por vírgulas)", "*.csv"),
    ("Texto separado por tabulações", "*.txt"),
    ("Todos os arquivos", "*.*")
]

def salvar(nome):
    caminho = filedialog.asksaveasfilename(
        initialfile= nome,
        defaultextension=".xlsx", 
        filetypes = tipos_excel,
        title="Salvar Padrões"
        )

    return caminho
    
def gerar_padroes(L, cortes):
        menor_corte = min(cortes) # Obtem o tamanho do menor corte
        limites = [range((L // c) + 1) for c in cortes]                                                        
        
        padroes = [] # lista para armazenar os padrões de corte possiveis
        perdas = []  # lista para armazenar as perdas dos padrões de corte possiveis

        for combinacao in product(*limites): # O product faz o plano cartesiano para cada RANGE em limites

            total = sum(qtd * tamanho for qtd, tamanho in zip(combinacao, cortes))  
            perda = L - total

            if 0 < total <= L and perda < menor_corte:
                padroes.append(list(combinacao))
                perdas.append(perda)
        return padroes, perdas


# Fonte em negrito
negrito = Font(bold=True)

# Mudando a cor de fundo
# A cor deve ser passada em formato hexadecimal ARGB. Ex: Amarelo = "FFFF00"
cor_fundo_descartado = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="darkVertical") # Amarelo
cor_fundo_usado = PatternFill(start_color="FF28A745", end_color="FF28A745", fill_type="lightVertical") # Verde
cor_fundo_header = PatternFill(start_color="2F4F4F", end_color="2F4F4F", fill_type="darkGray") # cinza

# Centralizando o conteúdo
alinhamento = Alignment(horizontal="center", vertical="center")

# Colocando borda
# Primeiro definimos o estilo da linha (fina e preta), depois aplicamos aos 4 lados da célula
linha_fina = Side(border_style="thin", color="000000")
linha_medium = Side(border_style="medium", color="000000")

borda_fina = Border(left=linha_fina, right=linha_fina, top=linha_fina, bottom=linha_fina)
borda_medium = Border(left=linha_medium, right=linha_medium, top=linha_medium, bottom=linha_medium)
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

# Cria uma nova pasta de trabalho (Workbook)
wb = Workbook()

# Seleciona a aba ativa
ws = wb.active
ws.title = "Padrões"

# Adiciona o cabeçalho
ws["A1"] = "ID"
ws["B1"] = "50 cm"
ws["C1"] = "40 cm"
ws["D1"] = "30 cm"
ws["E1"] = "Perda (cm)"

# Alenta um pouco a largura da celula
ws.column_dimensions["E"].width = 17

Q, perda = gerar_padroes(130, [50, 40, 30])

# Adiciona dados nas linhas
for id, x in enumerate(zip(Q, perda)): 
    ws.append([id+1, *x[0], x[1]])


# Percorre todas as linhas e colunas que possuem dados para aplicar a formatação célula por célula
for linha in ws.iter_cols(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for x, celula in enumerate(linha):
        
        if not x: # Cabeçalho
            celula.fill = cor_fundo_header
            celula.alignment = alinhamento
            celula.border = borda_medium
            celula.font = negrito
        else: 
            if x in [2, 3 , 6]: # Padroes usados
                celula.fill = cor_fundo_usado
                celula.alignment = alinhamento
                celula.border = borda_fina
            else: # Padroes não usados
                celula.fill = cor_fundo_descartado
                celula.alignment = alinhamento
                celula.border = borda_fina
            

# Escolhe o caminho que quer salvar 
caminho_salvar = salvar("instancia_4")

# Salva o arquivo Excel
wb.save(caminho_salvar)
