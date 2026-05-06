import os
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# =========================
# CONFIG
# =========================

ARQUIVO_LINKS = "links.txt"
ARQUIVO_SAIDA = "base_final.json"

API_URL = "http://localhost:20128/v1/chat/completions"
MODEL = "gpt-5.3-codex"

# =========================
# PROMPT (BASE CONHECIMENTO)
# =========================

PROMPT = """
Você é um especialista no sistema FarmaFácil.

Transforme o conteúdo abaixo em JSON estruturado.

REGRAS:
- Retorne APENAS JSON válido
- Não escreva nada fora do JSON
- Não invente informações

Formato:

{
  "tipo": "",
  "titulo": "",
  "descricao": "",
  "quando_usar": "",
  "como_funciona": "",
  "passos": [],
  "regras": [],
  "observacoes": [],
  "tags": []
}

Conteúdo:
"""

# =========================
# DRIVER
# =========================

def iniciar_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=options)

# =========================
# IA
# =========================

def chamar_ia(texto):
    try:
        r = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": PROMPT + texto}
                ],
                "temperature": 0.2
            },
            timeout=60
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Erro IA:", e)
        return None

# =========================
# EXTRAIR JSON
# =========================

def extrair_json(txt):
    try:
        inicio = txt.find("{")
        fim = txt.rfind("}") + 1
        return json.loads(txt[inicio:fim])
    except:
        return None

# =========================
# LIMPAR HTML
# =========================

def limpar_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()

    titulo = soup.find("h1")
    titulo = titulo.get_text().strip() if titulo else "Sem título"

    texto = soup.get_text("\n")
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]

    return titulo, "\n".join(linhas)

# =========================
# LINKS
# =========================

def carregar_links():
    links = []
    with open(ARQUIVO_LINKS, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.startswith("http"):
                links.append(linha.split()[0])
    return links

# =========================
# MAIN
# =========================

def main():
    links = carregar_links()

    # carregar progresso
    if os.path.exists(ARQUIVO_SAIDA):
        with open(ARQUIVO_SAIDA, "r", encoding="utf-8") as f:
            base = json.load(f)
    else:
        base = []

    ids_existentes = {item["id"] for item in base}

    driver = iniciar_driver()

    print("🔐 Faça login no Movidesk")
    driver.get("https://prismafive.movidesk.com")
    input("👉 Depois de logar, aperte ENTER")

    for i, url in enumerate(links):
        id_artigo = url.split("/")[-1]

        if id_artigo in ids_existentes:
            print(f"⏭ {id_artigo} já processado")
            continue

        print(f"⬇ {i+1}/{len(links)} - {id_artigo}")

        try:
            driver.get(url)
            time.sleep(3)

            html = driver.page_source

            titulo, conteudo = limpar_html(html)

            if len(conteudo) < 50:
                print("⚠ Conteúdo muito pequeno")
                continue

            # IA
            resposta = chamar_ia(conteudo)

            if resposta:
                print("🤖 IA respondeu")
            else:
                print("❌ IA não respondeu")

            json_final = extrair_json(resposta) if resposta else None

            # fallback
            if not json_final:
                print("⚠ Usando fallback")

                json_final = {
                    "tipo": "outro",
                    "titulo": titulo,
                    "descricao": conteudo[:500],
                    "quando_usar": None,
                    "como_funciona": None,
                    "passos": [],
                    "regras": [],
                    "observacoes": [],
                    "tags": []
                }

            # final
            json_final["id"] = id_artigo
            json_final["url"] = url
            json_final["titulo_original"] = titulo

            base.append(json_final)

            # salvar incremental
            with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
                json.dump(base, f, ensure_ascii=False, indent=2)

            print("✔ SALVO\n")

            time.sleep(1)

        except Exception as e:
            print("❌ Erro:", e)

    driver.quit()
    print("✅ FINALIZADO")

# =========================

if __name__ == "__main__":
    main()