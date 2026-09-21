# utils/auth.py
# Este ficheiro trata de fazer login no DVWA automaticamente
# e de definir o nível de dificuldade do site

import requests        # permite ao programa navegar em sites como um browser
from bs4 import BeautifulSoup  # permite ler o código HTML das páginas


def login_dvwa(base_url="http://localhost/dvwa", username="admin", password="password"):
    # Cria uma sessão — é como abrir um browser que guarda o login entre páginas
    # Sem isto, o programa esquecia que estava autenticado a cada pedido
    session = requests.Session()

    # Abre a página de login para ler um código de segurança escondido no formulário
    # Este código (token CSRF) muda sempre e prova que o pedido é legítimo
    login_page = session.get(f"{base_url}/login.php")
    soup = BeautifulSoup(login_page.text, "html.parser")
    token_input = soup.find("input", {"name": "user_token"})
    csrf_token = token_input["value"] if token_input else ""

    # Prepara os dados do formulário de login, como se preenchesses manualmente
    login_data = {
        "username": username,    # nome de utilizador
        "password": password,    # senha
        "Login": "Login",        # simula clicar no botão Login
        "user_token": csrf_token # código de segurança lido antes
    }

    # Envia o formulário — como clicar em "Entrar"
    session.post(f"{base_url}/login.php", data=login_data)

    # Devolve a sessão autenticada para ser usada nos ataques
    return session


def set_security_level(session, level="low"):
    # Muda o nível de dificuldade do DVWA (low, medium, high)
    # Isto controla quão bem o site se protege contra os ataques

    # Abre a página de segurança para ler o código de segurança necessário
    pagina = session.get("http://localhost/dvwa/security.php")
    soup = BeautifulSoup(pagina.text, "html.parser")
    token_input = soup.find("input", {"name": "user_token"})
    token = token_input["value"] if token_input else ""

    # Envia o pedido para mudar o nível
    session.post("http://localhost/dvwa/security.php", data={
        "security": level,           # o nível escolhido (low, medium, high)
        "seclev_submit": "Submit",   # simula clicar no botão
        "user_token": token          # código de segurança
    })