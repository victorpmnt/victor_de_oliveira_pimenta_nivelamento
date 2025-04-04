import pdfplumber 
import pandas as pd
from zipfile import ZipFile

# Caminho do PDF do Anexo I (usando o que baixamos antes)
pdf_path = "pdfs/anexo_1.pdf"

# Lista para armazenar as tabelas de cada página
tabelas = []

with pdfplumber.open(pdf_path) as pdf:
    for pagina in pdf.pages:
        tabela = pagina.extract_table()
        if tabela:
            df = pd.DataFrame(tabela[1:], columns=tabela[0])  # ignora header duplicado
            tabelas.append(df)

# Junta todas as páginas em um único DataFrame
df_final = pd.concat(tabelas, ignore_index=True)

# 2.4 Substituições
df_final.replace({"OD": "Odontologia", "AMB": "Ambulatorial"}, inplace=True)

# Salva em CSV
csv_path = "Teste_Victor_de_Oliveira_Pimenta.csv"
df_final.to_csv(csv_path, index=False)

# Compacta arquivo teste
with ZipFile(f"Teste_Victor_de_Oliveira_Pimenta.zip", "w") as zipf:
    zipf.write(csv_path)

print(df_final.head())

print("Tabela extraída, CSV salvo e compactado!")
