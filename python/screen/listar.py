from modules.mysql import MySQL
from modules.contatos import Contatos

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)


class Listar:

    def __init__(self, app):
        self.app = app
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        # ===== ESTILO DA TELA DE LISTAGEM =====
        self.janela.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Arial;
                font-size: 13px;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                gridline-color: #e0e0e0;
                selection-background-color: #d6eaf8;
                selection-color: black;
            }

            QHeaderView::section {
                background-color: #2e86de;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #aed6f1;
                color: black;
            }

            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 10px;
                padding: 12px;
                margin-top: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1e8449;
            }

            QPushButton:pressed {
                background-color: #186a3b;
            }
        """)
        # ====================================

        self.layout.setSpacing(12)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.configurar_janela()
        self.criar_componentes()
        self.carregar_dados()

    def configurar_janela(self):
        self.janela.setWindowTitle("Listagem de Contatos")

        screen = self.app.primaryScreen().geometry()
        largura = int(screen.width() * 0.6)
        altura = int(screen.height() * 0.7)

        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        self.tabela = QTableWidget()

        # 3 colunas
        self.tabela.setColumnCount(3)

        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Email",
            "Telefone"
        ])

        # Configurações de usabilidade
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSortingEnabled(True)
        self.tabela.horizontalHeader().setStretchLastSection(True)

        # Define largura mínima para cada coluna
        self.tabela.setColumnWidth(0, 150)  # Nome
        self.tabela.setColumnWidth(1, 250)  # Email
        self.tabela.setColumnWidth(2, 150)  # Telefone

        self.layout.addWidget(self.tabela)

        botao_atualizar = QPushButton("Atualizar")
        self.layout.addWidget(botao_atualizar)

        botao_atualizar.clicked.connect(self.carregar_dados)

    def carregar_dados(self):
        # Limpa tabela antes de recarregar
        self.tabela.setRowCount(0)

        self.banco.connect()
        contatos = Contatos.listar(self.banco)
        self.banco.disconnect()

        if not contatos:
            return

        # Define número de linhas
        self.tabela.setRowCount(len(contatos))

        # Preenche tabela
        for linha, contato in enumerate(contatos):
            self.tabela.setItem(linha, 0, QTableWidgetItem(contato["nome"]))
            self.tabela.setItem(linha, 1, QTableWidgetItem(contato["email"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(contato["telefone"]))

        # Ajusta largura das colunas de acordo com o conteúdo
        self.tabela.resizeColumnsToContents()