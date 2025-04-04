import pandas as pd
from sqlalchemy import create_engine

# Caminho do seu CSV
caminho_csv = "D:/Programas/MySQL/Data/Uploads/Relatorio_cadop.csv"

# Lê o CSV com separador e encoding apropriado
df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')

# Converte a coluna de data
df["Data_Registro_ANS"] = pd.to_datetime(df["Data_Registro_ANS"], errors="coerce")

# Renomeia as colunas para corresponder aos nomes da tabela no MySQL
df.columns = [
    "registro_ans", "cnpj", "razao_social", "nome_fantasia", "modalidade",
    "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep",
    "ddd", "telefone", "fax", "endereco_eletronico", "representante",
    "cargo_representante", "regiao_de_comercializacao", "data_registro_ans"
]


# Conexão com o MySQL (altere a senha se necessário)
engine = create_engine("mysql+mysqlconnector://root:Vi%40040604@localhost:3306/ans_dados")


# Envia os dados para o banco
df.to_sql("operadoras_ativas", con=engine, if_exists="append", index=False)

print("✅ Dados importados com sucesso!")