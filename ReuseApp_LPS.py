import csv
from datetime import datetime
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

# ==========================================================
# REUSEAPP - DEMONSTRAÇÃO DE COMPONENTES REUTILIZÁVEIS
# Protótipo em Python para explicar Linha de Produtos de Software (LPS)
# ==========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_FEEDBACK_CSV = BASE_DIR / "feedbacks_lps.csv"
ARQUIVO_FEEDBACK_TXT = BASE_DIR / "feedbacks_lps.txt"
ARQUIVO_RELATORIO_TXT = BASE_DIR / "relatorio_lps.txt"


# ==========================================================
# VARIABILIDADE DA LINHA DE PRODUTOS DE SOFTWARE
# ==========================================================
# Aqui ficam as diferenças entre os produtos da mesma família.
# A base é a mesma, mas mudam nome, cor, produtos, tipo de cadastro,
# tipo de pedido e formas de pagamento.

CONFIGURACOES = {
    "Lanchonete": {
        "nome_app": "ReuseApp - Lanchonete",
        "descricao": "Sistema de pedidos para lanchonete.",
        "cor": "#ff9800",
        "tipo_cadastro": "Cliente",
        "tipo_lista": "Cardápio",
        "tipo_pedido": "Pedido de Hambúrguer",
        "produtos": [
            {"nome": "Hambúrguer", "categoria": "Comida", "preco": 18.00},
            {"nome": "Batata Frita", "categoria": "Comida", "preco": 10.00},
            {"nome": "Refrigerante", "categoria": "Bebida", "preco": 6.00},
            {"nome": "Combo Completo", "categoria": "Combo", "preco": 32.00},
        ],
        "pagamentos": ["Pix", "Cartão", "Dinheiro"],
    },

    "Loja de Roupas": {
        "nome_app": "ReuseApp - Loja de Roupas",
        "descricao": "Sistema de catálogo e venda para loja de roupas.",
        "cor": "#3f51b5",
        "tipo_cadastro": "Cliente",
        "tipo_lista": "Catálogo de Produtos",
        "tipo_pedido": "Pedido de Compra",
        "produtos": [
            {"nome": "Camisa", "categoria": "Roupa", "preco": 50.00},
            {"nome": "Calça Jeans", "categoria": "Roupa", "preco": 120.00},
            {"nome": "Tênis", "categoria": "Calçado", "preco": 180.00},
            {"nome": "Boné", "categoria": "Acessório", "preco": 35.00},
        ],
        "pagamentos": ["Pix", "Cartão"],
    },

    "Barbearia": {
        "nome_app": "ReuseApp - Barbearia",
        "descricao": "Sistema de serviços e solicitações para barbearia.",
        "cor": "#009688",
        "tipo_cadastro": "Cliente",
        "tipo_lista": "Lista de Serviços",
        "tipo_pedido": "Solicitação de Serviço",
        "produtos": [
            {"nome": "Corte de Cabelo", "categoria": "Serviço", "preco": 35.00},
            {"nome": "Barba", "categoria": "Serviço", "preco": 25.00},
            {"nome": "Corte + Barba", "categoria": "Combo", "preco": 55.00},
            {"nome": "Sobrancelha", "categoria": "Serviço", "preco": 15.00},
        ],
        "pagamentos": ["Pix", "Cartão", "Dinheiro"],
    },

    "Assistência Técnica": {
        "nome_app": "ReuseApp - Assistência Técnica",
        "descricao": "Sistema de chamados e serviços técnicos.",
        "cor": "#9c27b0",
        "tipo_cadastro": "Usuário",
        "tipo_lista": "Lista de Serviços Técnicos",
        "tipo_pedido": "Chamado Técnico",
        "produtos": [
            {"nome": "Formatação", "categoria": "Computador", "preco": 80.00},
            {"nome": "Troca de Tela", "categoria": "Celular", "preco": 250.00},
            {"nome": "Limpeza Interna", "categoria": "Computador", "preco": 100.00},
            {"nome": "Instalação de Sistema", "categoria": "Software", "preco": 60.00},
        ],
        "pagamentos": ["Pix", "Cartão"],
    },
}


FEATURE_MODEL = """
ReuseApp
├── Home [Obrigatório]
├── Login [Obrigatório]
├── Cadastro [Obrigatório]
├── Produtos/Serviços [Obrigatório]
├── Pedidos/Solicitações [Obrigatório]
├── Sobre LPS [Obrigatório]
├── Feedback [Opcional]
└── Variação do negócio [XOR]
    ├── Lanchonete
    ├── Loja de Roupas
    ├── Barbearia
    └── Assistência Técnica
""".strip()


# ==========================================================
# COMPONENTES REUTILIZÁVEIS - ATIVOS-BASE DA LPS
# ==========================================================
# Estes componentes são usados em várias telas do sistema.

class Header(ctk.CTkFrame):
    def __init__(self, master, titulo, subtitulo, cor):
        super().__init__(master, fg_color="transparent")

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 28, "bold"),
            text_color=cor
        )
        self.label_titulo.pack(anchor="w")

        self.label_subtitulo = ctk.CTkLabel(
            self,
            text=subtitulo,
            font=("Arial", 15),
            text_color="#d0d0d0",
            wraplength=850,
            justify="left"
        )
        self.label_subtitulo.pack(anchor="w", pady=(5, 0))


class AppButton(ctk.CTkButton):
    def __init__(self, master, texto, comando=None, cor="#1f6aa5"):
        super().__init__(
            master,
            text=texto,
            command=comando,
            height=42,
            corner_radius=10,
            fg_color=cor,
            hover_color="#333333",
            font=("Arial", 14, "bold")
        )


class AppInput(ctk.CTkEntry):
    def __init__(self, master, placeholder, senha=False):
        super().__init__(
            master,
            placeholder_text=placeholder,
            height=42,
            corner_radius=10,
            font=("Arial", 14),
            show="*" if senha else ""
        )


class ProductCard(ctk.CTkFrame):
    def __init__(self, master, produto, cor, comando_adicionar):
        super().__init__(master, corner_radius=12)
        self.produto = produto

        frame_info = ctk.CTkFrame(self, fg_color="transparent")
        frame_info.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        label_nome = ctk.CTkLabel(
            frame_info,
            text=produto["nome"],
            font=("Arial", 17, "bold"),
            anchor="w"
        )
        label_nome.pack(anchor="w")

        label_categoria = ctk.CTkLabel(
            frame_info,
            text=f"Categoria: {produto['categoria']}",
            font=("Arial", 13),
            text_color="#bdbdbd",
            anchor="w"
        )
        label_categoria.pack(anchor="w", pady=(4, 0))

        label_preco = ctk.CTkLabel(
            self,
            text=f"R$ {produto['preco']:.2f}",
            font=("Arial", 16, "bold"),
            text_color=cor
        )
        label_preco.pack(side="left", padx=10)

        botao = AppButton(
            self,
            "Adicionar",
            comando=lambda: comando_adicionar(produto),
            cor=cor
        )
        botao.pack(side="right", padx=15, pady=12)


# ==========================================================
# APLICAÇÃO PRINCIPAL
# ==========================================================

class ReuseAppLPS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ReuseApp - Demonstração de Componentes Reutilizáveis")
        self.geometry("1400x800")
        self.resizable(False, False)

        self.config_nome = "Lanchonete"
        self.config_atual = CONFIGURACOES[self.config_nome]
        self.tela_atual = "home"

        self.pedido = []
        self.feedbacks = []
        self.carregar_feedbacks_existentes()

        self.criar_layout()
        self.mostrar_home()

    # ======================================================
    # LAYOUT Base
    # ======================================================

    def criar_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=265, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.conteudo = ctk.CTkFrame(self, corner_radius=15)
        self.conteudo.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.criar_menu_lateral()

    def criar_menu_lateral(self):
        titulo = ctk.CTkLabel(
            self.sidebar,
            text="ReuseApp LPS",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=(25, 5))

        subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Componentes Reutilizáveis\ne Variabilidade",
            font=("Arial", 14),
            justify="center",
            text_color="#cfcfcf"
        )
        subtitulo.pack(pady=(0, 20))

        label_variacao = ctk.CTkLabel(
            self.sidebar,
            text="Variação da LPS:",
            font=("Arial", 14, "bold")
        )
        label_variacao.pack(pady=(10, 5))

        self.combo_variacao = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(CONFIGURACOES.keys()),
            command=self.alterar_variacao,
            width=215
        )
        self.combo_variacao.pack(pady=(0, 20))
        self.combo_variacao.set(self.config_nome)

        botoes = [
            ("1. Home", self.mostrar_home),
            ("2. Login", self.mostrar_login),
            ("3. Cadastro", self.mostrar_cadastro),
            ("4. Produtos/Serviços", self.mostrar_produtos),
            ("5. Pedidos/Solicitações", self.mostrar_pedidos),
            ("6. Sobre LPS", self.mostrar_sobre_lps),
            ("7. Feedback", self.mostrar_feedback),
        ]

        for texto, comando in botoes:
            botao = AppButton(self.sidebar, texto, comando)
            botao.pack(fill="x", padx=20, pady=5)

        explicacao = ctk.CTkLabel(
            self.sidebar,
            text=(
                "Conceitos aplicados:\n\n"
                "• Reuso\n"
                "• Ativos-base\n"
                "• Variabilidade\n"
                "• Feature Model\n"
                "• Engenharia de domínio\n"
                "• Engenharia de aplicação"
            ),
            font=("Arial", 13),
            justify="left",
            text_color="#cfcfcf"
        )
        explicacao.pack(pady=25, padx=25, anchor="w")

    # ======================================================
    # FUNÇÕES GERAIS
    # ======================================================

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def alterar_variacao(self, nome):
        self.config_nome = nome
        self.config_atual = CONFIGURACOES[nome]
        self.pedido.clear()

        if self.tela_atual == "home":
            self.mostrar_home()
        elif self.tela_atual == "login":
            self.mostrar_login()
        elif self.tela_atual == "cadastro":
            self.mostrar_cadastro()
        elif self.tela_atual == "produtos":
            self.mostrar_produtos()
        elif self.tela_atual == "pedidos":
            self.mostrar_pedidos()
        elif self.tela_atual == "sobre_lps":
            self.mostrar_sobre_lps()
        elif self.tela_atual == "feedback":
            self.mostrar_feedback()

    def calcular_total(self):
        return sum(item["preco"] for item in self.pedido)

    def criar_card_conceito(self, master, titulo, texto, cor):
        card = ctk.CTkFrame(master, corner_radius=12)
        card.pack(side="left", fill="both", expand=True, padx=8)

        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 18, "bold"),
            text_color=cor
        )
        label_titulo.pack(anchor="w", padx=15, pady=(15, 5))

        label_texto = ctk.CTkLabel(
            card,
            text=texto,
            font=("Arial", 14),
            wraplength=230,
            justify="left"
        )
        label_texto.pack(anchor="w", padx=15, pady=(0, 15))

    # ======================================================
    # 1. TELA HOME
    # ======================================================

    def mostrar_home(self):
        self.tela_atual = "home"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            "Home",
            "Objetivo do app: demonstrar como componentes reutilizáveis podem gerar produtos diferentes dentro de uma Linha de Produtos de Software.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        texto = (
            f"Produto selecionado: {self.config_atual['nome_app']}\n\n"
            "O ReuseApp é um protótipo criado para demonstrar como uma base comum de telas e componentes "
            "pode ser reaproveitada em vários sistemas: lanchonete, loja de roupas, barbearia e assistência técnica.\n\n"
            "Na LPS, a base comum representa os ativos-base. As diferenças entre os produtos representam a variabilidade. "
            "Neste app, a variabilidade muda nome, cor, tipo de cadastro, produtos, serviços, pedidos e formas de pagamento."
        )

        label_texto = ctk.CTkLabel(
            self.conteudo,
            text=texto,
            font=("Arial", 16),
            justify="left",
            wraplength=850
        )
        label_texto.pack(anchor="w", padx=35, pady=10)

        frame_cards = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        frame_cards.pack(fill="x", padx=30, pady=25)

        self.criar_card_conceito(
            frame_cards,
            "Ativos-base",
            "Header, AppButton, AppInput, ProductCard e telas reutilizáveis.",
            cor
        )

        self.criar_card_conceito(
            frame_cards,
            "Variabilidade",
            "Mudança de nome, cor, produtos, serviços, pagamentos e contexto.",
            cor
        )

        self.criar_card_conceito(
            frame_cards,
            "Produto final",
            "A mesma base gera Lanchonete, Loja, Barbearia e Assistência Técnica.",
            cor
        )

        botao_sobre = AppButton(
            self.conteudo,
            "Ver explicação acadêmica de LPS",
            self.mostrar_sobre_lps,
            cor
        )
        botao_sobre.pack(anchor="w", padx=35, pady=15)

    # ======================================================
    # 2. TELA LOGIN
    # ======================================================

    def mostrar_login(self):
        self.tela_atual = "login"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            "Login Reutilizável",
            "Esta tela de login pode ser reaproveitada em vários sistemas da mesma família.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        frame_form = ctk.CTkFrame(self.conteudo, corner_radius=15)
        frame_form.pack(padx=30, pady=20, fill="x")

        label = ctk.CTkLabel(
            frame_form,
            text=f"Entrar em: {self.config_atual['nome_app']}",
            font=("Arial", 20, "bold"),
            text_color=cor
        )
        label.pack(pady=(25, 15))

        self.input_login_email = AppInput(frame_form, "E-mail ou usuário")
        self.input_login_email.pack(fill="x", padx=40, pady=8)

        self.input_login_senha = AppInput(frame_form, "Senha", senha=True)
        self.input_login_senha.pack(fill="x", padx=40, pady=8)

        botao_entrar = AppButton(frame_form, "Entrar", self.acao_login, cor)
        botao_entrar.pack(fill="x", padx=40, pady=(15, 25))

        explicacao = ctk.CTkLabel(
            self.conteudo,
            text=(
                "LPS aplicada: o mesmo componente de login pode ser usado em app de lanchonete, loja, "
                "barbearia ou assistência técnica. A estrutura é igual; muda apenas o contexto do produto."
            ),
            font=("Arial", 14),
            text_color="#cfcfcf",
            wraplength=850,
            justify="left"
        )
        explicacao.pack(anchor="w", padx=35, pady=10)

    def acao_login(self):
        email = self.input_login_email.get().strip()
        if email == "":
            messagebox.showwarning("Atenção", "Digite um e-mail ou usuário.")
            return
        messagebox.showinfo("Login", f"Login demonstrativo realizado no produto:\n{self.config_atual['nome_app']}")

    # ======================================================
    # 3. TELA CADASTRO
    # ======================================================

    def mostrar_cadastro(self):
        self.tela_atual = "cadastro"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]
        tipo = self.config_atual["tipo_cadastro"]

        header = Header(
            self.conteudo,
            "Cadastro Reutilizável",
            f"Esta tela pode servir para cadastro de cliente, funcionário ou usuário. Nesta variação: Cadastro de {tipo}.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        frame_form = ctk.CTkFrame(self.conteudo, corner_radius=15)
        frame_form.pack(padx=30, pady=10, fill="x")

        label = ctk.CTkLabel(frame_form, text=f"Cadastro de {tipo}", font=("Arial", 20, "bold"), text_color=cor)
        label.pack(pady=(25, 15))

        self.input_nome = AppInput(frame_form, f"Nome do {tipo}")
        self.input_nome.pack(fill="x", padx=40, pady=8)

        self.input_email = AppInput(frame_form, "E-mail")
        self.input_email.pack(fill="x", padx=40, pady=8)

        self.input_telefone = AppInput(frame_form, "Telefone")
        self.input_telefone.pack(fill="x", padx=40, pady=8)

        botao_salvar = AppButton(frame_form, "Salvar Cadastro", self.acao_cadastro, cor)
        botao_salvar.pack(fill="x", padx=40, pady=(15, 25))

        explicacao = ctk.CTkLabel(
            self.conteudo,
            text=(
                "LPS aplicada: a tela de cadastro é um ativo-base. Ela pode ser reutilizada com pequenas "
                "variações, como cadastro de cliente, usuário ou funcionário."
            ),
            font=("Arial", 14),
            text_color="#cfcfcf",
            wraplength=850,
            justify="left"
        )
        explicacao.pack(anchor="w", padx=35, pady=10)

    def acao_cadastro(self):
        nome = self.input_nome.get().strip()
        if nome == "":
            messagebox.showwarning("Atenção", "Digite um nome para o cadastro.")
            return
        messagebox.showinfo("Cadastro", f"Cadastro demonstrativo realizado com sucesso:\n{nome}")

    # ======================================================
    # 4. TELA LISTA DE PRODUTOS/SERVIÇOS
    # ======================================================

    def mostrar_produtos(self):
        self.tela_atual = "produtos"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            self.config_atual["tipo_lista"],
            "Esta tela usa o componente ProductCard. Ele pode representar hambúrguer, roupa, serviço ou chamado técnico.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        frame_lista = ctk.CTkScrollableFrame(self.conteudo, corner_radius=15)
        frame_lista.pack(fill="both", expand=True, padx=30, pady=10)

        for produto in self.config_atual["produtos"]:
            card = ProductCard(frame_lista, produto, cor, self.adicionar_ao_pedido)
            card.pack(fill="x", padx=10, pady=8)

    def adicionar_ao_pedido(self, produto):
        self.pedido.append(produto)
        messagebox.showinfo("Adicionado", f"{produto['nome']} foi adicionado em:\n{self.config_atual['tipo_pedido']}")

    # ======================================================
    # 5. TELA PEDIDOS/SOLICITAÇÕES
    # ======================================================

    def mostrar_pedidos(self):
        self.tela_atual = "pedidos"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            self.config_atual["tipo_pedido"],
            "Esta tela mostra como o mesmo componente de pedido pode ser adaptado para compra, solicitação ou chamado técnico.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        frame_pedido = ctk.CTkFrame(self.conteudo, corner_radius=15)
        frame_pedido.pack(fill="both", expand=True, padx=30, pady=10)

        self.texto_pedido = ctk.CTkTextbox(frame_pedido, height=260, font=("Arial", 15))
        self.texto_pedido.pack(fill="x", padx=25, pady=20)
        self.atualizar_texto_pedido()

        self.label_total = ctk.CTkLabel(
            frame_pedido,
            text=f"Total: R$ {self.calcular_total():.2f}",
            font=("Arial", 22, "bold"),
            text_color=cor
        )
        self.label_total.pack(anchor="w", padx=25, pady=10)

        self.combo_pagamento = ctk.CTkOptionMenu(frame_pedido, values=self.config_atual["pagamentos"], width=250)
        self.combo_pagamento.pack(anchor="w", padx=25, pady=10)
        self.combo_pagamento.set(self.config_atual["pagamentos"][0])

        frame_botoes = ctk.CTkFrame(frame_pedido, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=25, pady=20)

        botao_finalizar = AppButton(frame_botoes, "Finalizar", self.finalizar_pedido, cor)
        botao_finalizar.pack(side="left", padx=(0, 10))

        botao_limpar = AppButton(frame_botoes, "Limpar", self.limpar_pedido, "#b71c1c")
        botao_limpar.pack(side="left")

    def atualizar_texto_pedido(self):
        self.texto_pedido.configure(state="normal")
        self.texto_pedido.delete("1.0", "end")

        if len(self.pedido) == 0:
            self.texto_pedido.insert("end", "Nenhum item adicionado ainda.\n")
            self.texto_pedido.insert("end", "Vá na tela Produtos/Serviços e adicione um item.")
        else:
            self.texto_pedido.insert("end", "Itens adicionados:\n\n")
            for item in self.pedido:
                self.texto_pedido.insert("end", f"- {item['nome']} | {item['categoria']} | R$ {item['preco']:.2f}\n")

        self.texto_pedido.configure(state="disabled")

    def finalizar_pedido(self):
        if len(self.pedido) == 0:
            messagebox.showwarning("Atenção", "Adicione pelo menos um item antes de finalizar.")
            return

        pagamento = self.combo_pagamento.get()
        total = self.calcular_total()
        messagebox.showinfo(
            "Finalizado",
            f"{self.config_atual['tipo_pedido']} finalizado com sucesso!\n\n"
            f"Produto da LPS: {self.config_atual['nome_app']}\n"
            f"Forma de pagamento: {pagamento}\n"
            f"Total: R$ {total:.2f}"
        )
        self.limpar_pedido()

    def limpar_pedido(self):
        self.pedido.clear()
        if self.tela_atual == "pedidos":
            self.atualizar_texto_pedido()
            self.label_total.configure(text="Total: R$ 0.00")

    # ======================================================
    # 6. Tela LPS.
    # ======================================================

    def mostrar_sobre_lps(self):
        self.tela_atual = "sobre_lps"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            "Sobre LPS",
            "Explicação acadêmica do protótipo: onde aparecem reuso, ativos-base, variabilidade, Feature Model, engenharia de domínio e engenharia de aplicação.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        abas = ctk.CTkTabview(self.conteudo, corner_radius=15)
        abas.pack(fill="both", expand=True, padx=30, pady=10)
        abas.add("Conceitos")
        abas.add("Feature Model")
        abas.add("Mapeamento")

        texto_conceitos = (
            "Linha de Produtos de Software. (LPS) é uma estratégia de reuso sistemático para criar produtos de uma mesma família.\n\n"
            "Neste protótipo, a família de produtos é formada por sistemas de pedidos, catálogos e serviços. "
            "A base comum é composta por telas e componentes reutilizáveis. A variabilidade permite adaptar essa base "
            "para Lanchonete, Loja de Roupas, Barbearia e Assistência Técnica.\n\n"
            "Ativos-base: Header, AppButton, AppInput, ProductCard, telas de Login, Cadastro, Produtos e Pedidos.\n"
            "Variabilidade: nome do app, cor, produtos, serviços, tipo de cadastro, tipo de pedido e pagamentos.\n"
            "Engenharia de domínio: criação da base comum reutilizável.\n"
            "Engenharia de aplicação: escolha de uma variação para gerar um produto específico."
        )

        label_conceitos = ctk.CTkLabel(
            abas.tab("Conceitos"),
            text=texto_conceitos,
            font=("Arial", 15),
            justify="left",
            wraplength=820
        )
        label_conceitos.pack(anchor="w", padx=25, pady=25)

        textbox_feature = ctk.CTkTextbox(abas.tab("Feature Model"), font=("Consolas", 16))
        textbox_feature.pack(fill="both", expand=True, padx=25, pady=25)
        textbox_feature.insert("end", FEATURE_MODEL)
        textbox_feature.configure(state="disabled")

        texto_mapeamento = (
            "Conceito da LPS | Onde aparece no protótipo\n"
            "------------------------------------------------------------\n"
            "LPS | ReuseApp gera diferentes produtos da mesma família\n"
            "Ativos-base | Componentes Header, AppButton, AppInput e ProductCard\n"
            "Reuso | As mesmas telas são usadas para vários negócios\n"
            "Variabilidade | Dicionário CONFIGURACOES\n"
            "Produto final | Lanchonete, Loja, Barbearia ou Assistência Técnica\n"
            "Engenharia de domínio | Criação da base comum do app\n"
            "Engenharia de aplicação | Seleção da variação pelo menu lateral\n"
            "Feedback | Evidência da participação da comunidade"
        )

        textbox_mapa = ctk.CTkTextbox(abas.tab("Mapeamento"), font=("Consolas", 14))
        textbox_mapa.pack(fill="both", expand=True, padx=25, pady=25)
        textbox_mapa.insert("end", texto_mapeamento)
        textbox_mapa.configure(state="disabled")

    # ======================================================
    # 7. TELA Feedback
    # ======================================================

    def mostrar_feedback(self):
        self.tela_atual = "feedback"
        self.limpar_conteudo()
        cor = self.config_atual["cor"]

        header = Header(
            self.conteudo,
            "Feedback",
            "Esta tela coleta a resposta dos participantes. Os dados são salvos em CSV e TXT para servirem como evidência da atividade de extensão.",
            cor
        )
        header.pack(fill="x", padx=30, pady=25)

        frame_feedback = ctk.CTkFrame(self.conteudo, corner_radius=15)
        frame_feedback.pack(fill="x", padx=30, pady=10)

        pergunta = ctk.CTkLabel(
            frame_feedback,
            text="Você entendeu como componentes reutilizáveis se relacionam com LPS?",
            font=("Arial", 18, "bold"),
            wraplength=850,
            justify="left"
        )
        pergunta.pack(anchor="w", padx=25, pady=(25, 10))

        self.input_participante = AppInput(frame_feedback, "Nome ou identificação do participante")
        self.input_participante.pack(fill="x", padx=25, pady=8)

        self.combo_feedback = ctk.CTkOptionMenu(
            frame_feedback,
            values=["Sim, entendi", "Entendi parcialmente", "Ainda tenho dúvida"],
            width=260
        )
        self.combo_feedback.pack(anchor="w", padx=25, pady=8)
        self.combo_feedback.set("Sim, entendi")

        self.input_comentario = AppInput(frame_feedback, "Comentário do participante")
        self.input_comentario.pack(fill="x", padx=25, pady=8)

        frame_botoes = ctk.CTkFrame(frame_feedback, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=25, pady=(10, 25))

        botao_salvar = AppButton(frame_botoes, "Salvar Feedback", self.salvar_feedback, cor)
        botao_salvar.pack(side="left", padx=(0, 10))

        botao_exportar = AppButton(frame_botoes, "Exportar Relatório", self.exportar_relatorio, "#2e7d32")
        botao_exportar.pack(side="left")

        self.texto_feedbacks = ctk.CTkTextbox(self.conteudo, height=230, font=("Arial", 14))
        self.texto_feedbacks.pack(fill="x", padx=30, pady=20)
        self.atualizar_feedbacks()

    def carregar_feedbacks_existentes(self):
        if not ARQUIVO_FEEDBACK_CSV.exists():
            return
        try:
            with open(ARQUIVO_FEEDBACK_CSV, "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)
                self.feedbacks = list(leitor)
        except Exception:
            self.feedbacks = []

    def salvar_feedback(self):
        participante = self.input_participante.get().strip()
        resposta = self.combo_feedback.get()
        comentario = self.input_comentario.get().strip()

        if participante == "":
            participante = "Participante não identificado"
        if comentario == "":
            comentario = "Sem comentário."

        feedback = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "participante": participante,
            "produto": self.config_atual["nome_app"],
            "resposta": resposta,
            "comentario": comentario
        }

        self.feedbacks.append(feedback)
        self.salvar_feedback_csv(feedback)
        self.salvar_feedback_txt(feedback)

        messagebox.showinfo(
            "Feedback",
            f"Feedback salvo com sucesso.\n\nArquivos gerados:\n{ARQUIVO_FEEDBACK_CSV.name}\n{ARQUIVO_FEEDBACK_TXT.name}"
        )
        self.input_participante.delete(0, "end")
        self.input_comentario.delete(0, "end")
        self.atualizar_feedbacks()

    def salvar_feedback_csv(self, feedback):
        arquivo_existe = ARQUIVO_FEEDBACK_CSV.exists()
        with open(ARQUIVO_FEEDBACK_CSV, "a", newline="", encoding="utf-8") as arquivo:
            campos = ["data_hora", "participante", "produto", "resposta", "comentario"]
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            if not arquivo_existe:
                escritor.writeheader()
            escritor.writerow(feedback)

    def salvar_feedback_txt(self, feedback):
        with open(ARQUIVO_FEEDBACK_TXT, "a", encoding="utf-8") as arquivo:
            arquivo.write("=" * 70 + "\n")
            arquivo.write(f"Data/Hora: {feedback['data_hora']}\n")
            arquivo.write(f"Participante: {feedback['participante']}\n")
            arquivo.write(f"Produto da LPS: {feedback['produto']}\n")
            arquivo.write(f"Resposta: {feedback['resposta']}\n")
            arquivo.write(f"Comentário: {feedback['comentario']}\n")

    def atualizar_feedbacks(self):
        self.texto_feedbacks.configure(state="normal")
        self.texto_feedbacks.delete("1.0", "end")

        if len(self.feedbacks) == 0:
            self.texto_feedbacks.insert("end", "Nenhum feedback salvo ainda.")
        else:
            self.texto_feedbacks.insert("end", "Feedbacks registrados:\n\n")
            for i, feedback in enumerate(self.feedbacks, start=1):
                self.texto_feedbacks.insert(
                    "end",
                    f"{i}. {feedback.get('participante', 'Participante')} | {feedback.get('produto', '')}\n"
                    f"Resposta: {feedback.get('resposta', '')}\n"
                    f"Comentário: {feedback.get('comentario', '')}\n"
                    f"Data: {feedback.get('data_hora', '')}\n\n"
                )

        self.texto_feedbacks.configure(state="disabled")

    def exportar_relatorio(self):
        total_feedbacks = len(self.feedbacks)
        total_sim = sum(1 for f in self.feedbacks if f.get("resposta") == "Sim, entendi")
        total_parcial = sum(1 for f in self.feedbacks if f.get("resposta") == "Entendi parcialmente")
        total_duvida = sum(1 for f in self.feedbacks if f.get("resposta") == "Ainda tenho dúvida")

        conteudo = f"""
RELATÓRIO DA ATIVIDADE - REUSEAPP LPS
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

1. TEMA
Demonstração de componentes reutilizáveis em uma Linha de Produtos de Software.

2. OBJETIVO
Demonstrar como uma base comum de componentes pode ser reutilizada para gerar variações de sistemas para lanchonete, loja de roupas, barbearia e assistência técnica.

3. CONCEITOS APLICADOS
- Reuso de software
- Ativos-base
- Variabilidade
- Feature Model
- Engenharia de domínio
- Engenharia de aplicação

4. FEATURE MODEL
{FEATURE_MODEL}

5. PARTICIPAÇÃO E FEEDBACK
Total de feedbacks registrados: {total_feedbacks}
Sim, entendi: {total_sim}
Entendi parcialmente: {total_parcial}
Ainda tenho dúvida: {total_duvida}

6. RESULTADO ESPERADO
A atividade demonstra que componentes como Header, AppButton, AppInput e ProductCard podem ser reutilizados em diferentes sistemas, reduzindo retrabalho e facilitando a criação de produtos semelhantes dentro de uma mesma família de software.
""".strip()

        with open(ARQUIVO_RELATORIO_TXT, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

        messagebox.showinfo("Relatório exportado", f"Relatório salvo em:\n{ARQUIVO_RELATORIO_TXT}")


# ==========================================================
# EXECUTAR
# ==========================================================

if __name__ == "__main__":
    app = ReuseAppLPS()
    app.mainloop()
