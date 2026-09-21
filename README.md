# Scanner de Pentest — Controlo de Servidor

Ferramenta educativa de teste de segurança desenvolvida em Python.
Demonstra o impacto real de vulnerabilidades de Command Injection num ambiente controlado.

> ⚠️ **Uso exclusivamente educativo.** Testado apenas contra o DVWA (Damn Vulnerable Web Application), uma aplicação criada propositalmente para ser vulnerável. O uso desta ferramenta contra sistemas sem autorização é ilegal (Lei do Cibercrime, Lei n.º 109/2009).

---

## Funcionalidades

| # | Acção | Descrição |
|---|-------|-----------|
| 1 | Reconhecimento | Descobre utilizador, IP interno e utilizadores do servidor |
| 2 | Scan da Rede | Encontra dispositivos activos na rede interna |
| 3 | Scan de Portas | Analisa 16 portas num dispositivo encontrado |
| 4 | Ler Configurações | Lê ficheiros de configuração com credenciais |
| 5 | Ver Serviços | Lista todos os serviços Windows activos |
| 6 | Ver Ligações | Mostra ligações de rede activas (netstat) |

---

## Requisitos

- Python 3.11+
- XAMPP (Apache + MySQL)
- DVWA instalado em `C:\xampp\htdocs\dvwa`

---

## Instalação

### 1. Instalar Python
Descarrega em: https://www.python.org/downloads/
Durante a instalação, marca **"Add Python to PATH"**

### 2. Instalar XAMPP
Descarrega em: https://www.apachefriends.org/
Instala com as opções padrão.

### 3. Configurar o DVWA
1. Descarrega o DVWA: https://github.com/digininja/DVWA/archive/refs/heads/master.zip
2. Extrai e renomeia a pasta para `dvwa`
3. Copia para `C:\xampp\htdocs\dvwa`
4. Vai a `C:\xampp\htdocs\dvwa\config`
5. Copia `config.inc.php.dist` e renomeia a cópia para `config.inc.php`

### 4. Configurar a base de dados
1. Abre o XAMPP Control Panel
2. Clica **Start** em Apache e MySQL
3. Abre http://localhost/phpmyadmin
4. Clica em **SQL** e cola:
```sql
CREATE USER 'dvwa'@'%' IDENTIFIED BY 'p@ssw0rd';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'%';
FLUSH PRIVILEGES;
```
5. Abre http://localhost/dvwa/setup.php
6. Clica **"Create / Reset Database"**

### 5. Clonar o repositório e instalar dependências
```bash
git clone https://github.com/moniquemarrafon/pentest-server.git
cd pentest-server
pip install -r requirements.txt
```

---

## Como correr

```bash
python main.py
```

1. Escreve o URL do alvo (ex: `http://localhost/dvwa`)
2. Clica **LIGAR AO ALVO**
3. Escolhe uma das opções do menu de ações

---

## Estrutura

```
pentest-server/
├── main.py              # Interface gráfica principal
├── modules/
│   └── exploits.py      # Módulos de ataque
├── utils/
│   └── auth.py          # Autenticação no DVWA
├── requirements.txt
└── README.md
```

---

## Tecnologias

- **Python 3.11** — linguagem principal
- **tkinter** — interface gráfica
- **requests** — navegação HTTP
- **BeautifulSoup4** — análise de HTML
- **DVWA** — ambiente de teste

---

## Aviso Legal

Esta ferramenta foi desenvolvida exclusivamente para fins educativos e de teste autorizado.
O uso desta ferramenta contra sistemas sem autorização explícita é ilegal e pode constituir crime informático.
Testa apenas em ambientes que te pertencem ou para os quais tens autorização por escrito.

---

## Autora

**Monique Marrafon**
Curso Técnico de Programação e Sistemas de Informação
Porto, Portugal — 2026
