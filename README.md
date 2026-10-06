# Scanner de Pentest

Ferramenta educativa de teste de seguranca, desenvolvida em Python, com
interface grafica. Explora a vulnerabilidade de **Command Injection** no
DVWA para demonstrar o que um atacante conseguiria recolher de um servidor
que nao valida a entrada do utilizador.

> ⚠️ **Uso autorizado apenas.** Esta ferramenta foi feita para praticar
> contra o DVWA, um ambiente local criado de proposito para ser atacado.
> Usar contra sistemas sem autorizacao e ilegal.

---

## Funcionalidades

- **Ligar ao alvo** — faz login automatico no DVWA (com token CSRF) e define o nivel de seguranca.
- **Reconhecimento** — recolhe utilizador, IP interno, rede, contas do sistema e nome do servidor.
- **Scan da Rede** — procura dispositivos ativos na rede local (ping aos IPs .1 a .20).
- **Scan de Portas** — testa 16 portas comuns num dispositivo e indica quais estao abertas.
- **Ver Servicos** — lista os servicos que estao a correr na maquina.
- **Ver Ligacoes** — mostra as ligacoes de rede ativas (netstat).

Na apresentacao, os dados sensiveis (IP, nome da maquina e contas pessoais)
sao **camuflados**: o programa captura o valor real do alvo e so na hora de
mostrar no ecra troca por um nome generico.

---

## Tecnologias

- Python 3.11+
- Tkinter (interface grafica)
- requests (comunicacao HTTP)
- BeautifulSoup4 (leitura do HTML das respostas)

---

## Estrutura do projeto

```
scanner-pentest/
├── main.py              # Interface grafica e ligacao entre os modulos
├── modules/
│   └── exploits.py      # Logica dos ataques (reconhecimento, scans, etc.)
├── utils/
│   └── auth.py          # Login no DVWA e definicao do nivel de seguranca
├── requirements.txt     # Dependencias do projeto
├── DOCUMENTACAO.md      # Documentacao tecnica e academica
├── README.md
└── .gitignore
```

---

## Requisitos

- Python 3.11+
- XAMPP com Apache e MySQL
- DVWA em `C:\xampp\htdocs\dvwa`

## Instalacao

```bash
pip install -r requirements.txt
python main.py
```

## Configuracao do DVWA

1. Instala o XAMPP em https://www.apachefriends.org/
2. Inicia o Apache e o MySQL no XAMPP Control Panel
3. Descarrega o DVWA em https://github.com/digininja/DVWA
4. Copia a pasta para `C:\xampp\htdocs\dvwa`
5. Em `C:\xampp\htdocs\dvwa\config\`, copia `config.inc.php.dist` e renomeia para `config.inc.php`
6. Abre http://localhost/phpmyadmin e executa:
   ```sql
   CREATE USER 'dvwa'@'%' IDENTIFIED BY 'p@ssw0rd';
   GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'%';
   FLUSH PRIVILEGES;
   ```
7. Abre http://localhost/dvwa/setup.php e clica em **Create / Reset Database**
8. Faz login com `admin` / `password`

---

## Como usar

1. Inicia o DVWA (Apache + MySQL no XAMPP).
2. Corre `python main.py`.
3. Clica em **Ligar ao Alvo**.
4. Usa as acoes pela ordem: Reconhecimento → Scan da Rede → Scan de Portas → Ver Servicos → Ver Ligacoes.

---

## Licenca

MIT
