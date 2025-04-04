import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from zipfile import ZipFile

url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Requisição da página
res = requests.get(url_base)
res.raise_for_status()  # dispara erro se a requisição falhar

soup = BeautifulSoup(res.content, 'html.parser')

# criei diretório p/ PDFs
os.makedirs("pdfs", exist_ok=True)

# localizei os arquivos com palavras chave
keywords = ["anexo i", "anexo ii"]
pdf_links = []

# Procura por todos os links na página
for link in soup.find_all('a', href=True):
    texto_link = link.get_text(strip=True).lower()
    href = link['href']
    
    # Se o link contiver "anexo i" ou "anexo ii" E terminar em .pdf, salva
    if any(k in texto_link for k in keywords) and href.endswith(".pdf"):
        # Corrige link relativo
        full_url = urljoin(url_base, href)
        pdf_links.append((texto_link, full_url))

# Remover duplicatas
pdf_links = list(dict(pdf_links).items())[:2]

# Baixa os arquivos
pdf_paths = []
for idx, (label, link) in enumerate(pdf_links, start=1):
    nome_arquivo = f"pdfs/anexo_{idx}.pdf"
    print(f"Baixando {label.upper()}: {link}")
    r = requests.get(link)
    with open(nome_arquivo, "wb") as f:
        f.write(r.content)
    pdf_paths.append(nome_arquivo)

# Compacta em .zip
with ZipFile("anexos_rol_procedimentos.zip", "w") as zipf:
    for pdf in pdf_paths:
        zipf.write(pdf)

print("Todos os anexos foram baixados e compactados com sucesso!")
