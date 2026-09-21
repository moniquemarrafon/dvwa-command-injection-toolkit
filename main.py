# main.py

import tkinter as tk
from tkinter import scrolledtext
import threading

from utils.auth import login_dvwa, set_security_level
from modules.exploits import (
    reconhecimento, scan_rede, scan_portas,
    ler_config, listar_servicos, ver_ligacoes
)

# --- PALETA DE CORES ---
BG_ROOT         = "#0e1015"
BG_HEADER       = "#12141b"
BG_SURFACE      = "#171a22"
BG_SURFACE_HOVER= "#1e2330"
BORDER          = "#262b38"
ACCENT          = "#4f8cff"
ACCENT_HOVER    = "#3f78e0"
DANGER          = "#e5484d"
WARNING         = "#e0a53d"
SUCCESS         = "#3ecf8e"
TEXT_PRIMARY    = "#e7e9ee"
TEXT_SECONDARY  = "#9098ab"
TEXT_MUTED      = "#5b6274"
OUTPUT_BG       = "#0a0b0f"
OUTPUT_FG       = "#4ade80"

FONT_UI   = "Segoe UI"
FONT_MONO = "Consolas"


class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner de Pentest")
        self.root.geometry("1150x820")
        self.root.minsize(980, 700)
        self.root.configure(bg=BG_ROOT)
        self.session = None
        self.botoes_opcoes = []
        self.dispositivos_encontrados = []
        self.criar_interface()

    def criar_interface(self):
        self._criar_cabecalho()
        self._criar_barra_alvo()
        self._criar_menu()
        self._criar_output()
        self._criar_barra_estado()

    def _criar_cabecalho(self):
        cabecalho = tk.Frame(self.root, bg=BG_HEADER, pady=16)
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="SCANNER DE PENTEST",
            font=(FONT_UI, 17, "bold"),
            fg=TEXT_PRIMARY, bg=BG_HEADER
        ).pack()

        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x")

    def _criar_barra_alvo(self):
        cartao = tk.Frame(self.root, bg=BG_SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        cartao.pack(fill="x", padx=24, pady=(20, 12))

        interior = tk.Frame(cartao, bg=BG_SURFACE, pady=12, padx=16)
        interior.pack(fill="x")

        tk.Label(
            interior, text="ALVO",
            font=(FONT_UI, 9, "bold"),
            fg=TEXT_MUTED, bg=BG_SURFACE
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.campo_alvo = tk.Entry(
            interior, width=42,
            font=(FONT_MONO, 11),
            bg="#0f1319", fg=TEXT_PRIMARY,
            insertbackground=ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        self.campo_alvo.insert(0, "http://localhost/dvwa")
        self.campo_alvo.grid(row=0, column=1, ipady=6, padx=(0, 12), sticky="ew")

        self.btn_ligar = tk.Button(
            interior,
            text="LIGAR AO ALVO",
            font=(FONT_UI, 10, "bold"),
            bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", bd=0, cursor="hand2",
            padx=18, pady=8,
            command=self.ligar_ao_alvo
        )
        self.btn_ligar.grid(row=0, column=2, padx=(0, 16))
        self._hover(self.btn_ligar, ACCENT, ACCENT_HOVER)

        estado_frame = tk.Frame(interior, bg=BG_SURFACE)
        estado_frame.grid(row=0, column=3, sticky="e")

        self.indicador_estado = tk.Canvas(
            estado_frame, width=10, height=10,
            bg=BG_SURFACE, highlightthickness=0
        )
        self.indicador_estado.pack(side="left", padx=(0, 6))
        self._circulo = self.indicador_estado.create_oval(1, 1, 9, 9,
                                                          fill=TEXT_MUTED, outline="")

        self.label_estado = tk.Label(
            estado_frame, text="Desligado",
            font=(FONT_UI, 10),
            fg=TEXT_SECONDARY, bg=BG_SURFACE
        )
        self.label_estado.pack(side="left")
        interior.grid_columnconfigure(1, weight=1)

    def _criar_menu(self):
        secao = tk.Frame(self.root, bg=BG_ROOT)
        secao.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(
            secao, text="AÇÕES DISPONÍVEIS",
            font=(FONT_UI, 9, "bold"),
            fg=TEXT_MUTED, bg=BG_ROOT
        ).pack(anchor="w", pady=(0, 8))

        grelha = tk.Frame(secao, bg=BG_ROOT)
        grelha.pack(fill="x")
        for col in range(3):
            grelha.grid_columnconfigure(col, weight=1, uniform="col")

        opcoes = [
            ("🔎", "Reconhecimento",    self.opcao_reconhecimento, ACCENT),
            ("🌐", "Scan da Rede",      self.opcao_scan_rede,      ACCENT),
            ("🔌", "Scan de Portas",    self.opcao_scan_portas,    ACCENT),
            ("🔑", "Ler Configurações", self.opcao_ler_config,     WARNING),
            ("🖥",  "Ver Serviços",      self.opcao_listar_servicos, ACCENT),
            ("🔗", "Ver Ligações",      self.opcao_ver_ligacoes,   ACCENT),
        ]

        for i, (icone, titulo, comando, cor) in enumerate(opcoes):
            linha, coluna = divmod(i, 3)
            self._criar_cartao(grelha, icone, titulo, comando, cor, linha, coluna)

    def _criar_cartao(self, pai, icone, titulo, comando, cor, linha, coluna):
        wrapper = tk.Frame(pai, bg=BG_ROOT)
        wrapper.grid(row=linha, column=coluna, sticky="nsew", padx=6, pady=6)

        cartao = tk.Frame(wrapper, bg=BG_SURFACE,
                          highlightthickness=1, highlightbackground=BORDER)
        cartao.pack(fill="both", expand=True)

        tk.Frame(cartao, bg=cor, width=3).pack(side="left", fill="y")

        btn = tk.Button(
            cartao,
            text=f"{icone}  {titulo}",
            font=(FONT_UI, 10),
            bg=BG_SURFACE, fg=TEXT_PRIMARY,
            activebackground=BG_SURFACE_HOVER, activeforeground=TEXT_PRIMARY,
            relief="flat", bd=0, cursor="hand2",
            anchor="w", padx=14, pady=14,
            state="disabled", disabledforeground=TEXT_MUTED,
            command=comando
        )
        btn.pack(side="left", fill="both", expand=True)
        self._hover(btn, BG_SURFACE, BG_SURFACE_HOVER, cartao=cartao)
        self.botoes_opcoes.append(btn)

    def _criar_output(self):
        frame = tk.Frame(self.root, bg=BG_ROOT)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        tk.Label(
            frame, text="OUTPUT",
            font=(FONT_UI, 9, "bold"),
            fg=TEXT_MUTED, bg=BG_ROOT
        ).pack(anchor="w", pady=(0, 6))

        moldura = tk.Frame(frame, bg=OUTPUT_BG,
                           highlightthickness=1, highlightbackground=BORDER)
        moldura.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            moldura,
            font=(FONT_MONO, 11),
            bg=OUTPUT_BG, fg=OUTPUT_FG,
            insertbackground=TEXT_PRIMARY,
            relief="flat", bd=0,
            padx=14, pady=10,
            state="disabled",
            height=20
        )
        self.output.pack(fill="both", expand=True, padx=1, pady=1)

    def _criar_barra_estado(self):
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", side="bottom")
        self.barra_estado = tk.Label(
            self.root,
            text="Pronto — liga ao alvo para começar",
            font=(FONT_UI, 9),
            fg=TEXT_SECONDARY, bg=BG_HEADER,
            anchor="w", padx=24, pady=8
        )
        self.barra_estado.pack(fill="x", side="bottom")

    # ------------------------------------------------------------------
    def _hover(self, btn, normal, hover, cartao=None):
        def entrar(_):
            if btn["state"] == "normal":
                btn.config(bg=hover)
                if cartao: cartao.config(bg=hover)
        def sair(_):
            btn.config(bg=normal if btn["state"] == "normal" else BG_SURFACE)
            if cartao: cartao.config(bg=BG_SURFACE)
        btn.bind("<Enter>", entrar)
        btn.bind("<Leave>", sair)

    def log(self, msg):
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.config(state="disabled")
        self.root.update_idletasks()

    def limpar_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    def desactivar_botoes(self):
        for b in self.botoes_opcoes: b.config(state="disabled")

    def activar_botoes(self):
        for b in self.botoes_opcoes: b.config(state="normal")

    def _set_estado(self, ligado, texto):
        cor = SUCCESS if ligado else TEXT_MUTED
        self.indicador_estado.itemconfig(self._circulo, fill=cor)
        self.label_estado.config(text=texto,
                                  fg=SUCCESS if ligado else TEXT_SECONDARY)

    # ------------------------------------------------------------------
    def ligar_ao_alvo(self):
        alvo = self.campo_alvo.get()
        self.limpar_output()
        self.log(f"A ligar a {alvo}...")
        self.desactivar_botoes()

        def tarefa():
            try:
                self.session = login_dvwa(alvo)
                set_security_level(self.session, "low")
                self._set_estado(True, "Ligado")
                self.barra_estado.config(text=f"Ligado a {alvo}")
                self.activar_botoes()
                self.log(f"✅ Ligado a {alvo}\n")
            except Exception as e:
                self.log(f"❌ Erro: {e}")
                self.barra_estado.config(text="Erro na ligação")

        threading.Thread(target=tarefa, daemon=True).start()

    def opcao_reconhecimento(self):
        self.limpar_output()
        self.log("─── RECONHECIMENTO ───────────────────────────\n")
        self.desactivar_botoes()
        def tarefa():
            reconhecimento(self.session, "low", callback=self.log)
            self.log("\n✅ Concluído.")
            self.activar_botoes()
        threading.Thread(target=tarefa, daemon=True).start()

    def opcao_scan_rede(self):
        self.limpar_output()
        self.log("─── SCAN DA REDE ─────────────────────────────\n")
        self.desactivar_botoes()
        def tarefa():
            resultado = scan_rede(self.session, "low", callback=self.log)
            self.dispositivos_encontrados = resultado.get("dispositivos", [])
            self.log("\n✅ Concluído.")
            self.activar_botoes()
        threading.Thread(target=tarefa, daemon=True).start()

    def opcao_scan_portas(self):
        self.limpar_output()
        self.log("─── SCAN DE PORTAS ───────────────────────────\n")

        janela = tk.Toplevel(self.root)
        janela.title("Scan de Portas")
        janela.geometry("400x160")
        janela.configure(bg=BG_ROOT)
        janela.resizable(False, False)

        tk.Label(janela, text="IP do dispositivo:",
                 font=(FONT_UI, 11), fg=TEXT_PRIMARY, bg=BG_ROOT
                 ).pack(pady=(20, 8))

        campo_ip = tk.Entry(janela, font=(FONT_MONO, 11),
                            bg="#0f1319", fg=TEXT_PRIMARY, width=26,
                            relief="flat", highlightthickness=1,
                            highlightbackground=BORDER, highlightcolor=ACCENT,
                            justify="center")
        ip_auto = self.dispositivos_encontrados[0] if self.dispositivos_encontrados else "192.168.1.1"
        campo_ip.insert(0, ip_auto)
        campo_ip.pack(ipady=6)

        def confirmar():
            ip = campo_ip.get()
            janela.destroy()
            self.desactivar_botoes()
            def tarefa():
                scan_portas(self.session, ip, "low", callback=self.log)
                self.log("\n✅ Concluído.")
                self.activar_botoes()
            threading.Thread(target=tarefa, daemon=True).start()

        btn = tk.Button(janela, text="INICIAR", font=(FONT_UI, 10, "bold"),
                        bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
                        relief="flat", bd=0, cursor="hand2",
                        padx=16, pady=8, command=confirmar)
        btn.pack(pady=14)
        self._hover(btn, ACCENT, ACCENT_HOVER)

    def opcao_ler_config(self):
        self.limpar_output()
        self.log("─── LER CONFIGURAÇÕES ────────────────────────\n")
        self.desactivar_botoes()
        def tarefa():
            ler_config(self.session, "low", callback=self.log)
            self.log("\n✅ Concluído.")
            self.activar_botoes()
        threading.Thread(target=tarefa, daemon=True).start()

    def opcao_listar_servicos(self):
        self.limpar_output()
        self.log("─── VER SERVIÇOS ─────────────────────────────\n")
        self.desactivar_botoes()
        def tarefa():
            listar_servicos(self.session, "low", callback=self.log)
            self.log("\n✅ Concluído.")
            self.activar_botoes()
        threading.Thread(target=tarefa, daemon=True).start()

    def opcao_ver_ligacoes(self):
        self.limpar_output()
        self.log("─── VER LIGAÇÕES ─────────────────────────────\n")
        self.desactivar_botoes()
        def tarefa():
            ver_ligacoes(self.session, "low", callback=self.log)
            self.log("\n✅ Concluído.")
            self.activar_botoes()
        threading.Thread(target=tarefa, daemon=True).start()



if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()
