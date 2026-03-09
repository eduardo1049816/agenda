from modules.mysql import MySQL
from screen.editar import Editar
from modules.contatos import Contatos

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

class Listar:
    
    def __init__(self, app, callback_voltar):
        self.app = app
        self.callback_voltar = callback_voltar
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        # ===== ESTILO DA TABELA MODO ESCURO =====
        self.janela.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: Arial;
                font-size: 13px;
                color: #e5e7eb;
            }

            QTableWidget {
                background-color: #1f2937;
                color: #ffffff;
                border: 1px solid #374151;
                gridline-color: #374151;
                selection-background-color: #3b82f6; /* Azul ao selecionar linha */
                selection-color: white;
                alternate-background-color: #18202b; /* Cor da linha alternada */
            }

            QHeaderView::section {
                background-color: #111827; /* Topo da tabela bem escuro */
                color: #9ca3af;
                padding: 8px;
                border: 1px solid #374151;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QPushButton {
                background-color: #10b981; /* Verde esmeralda */
                color: white;
                border-radius: 10px;
                padding: 12px;
                margin-top: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
        """)

        self.layout.setSpacing(12)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.configurar_janela()
        self.criar_componentes()
        
        try:
            self.carregar_dados()
        except Exception:
            pass 

    def configurar_janela(self):
        self.janela.setWindowTitle("Listagem de Contatos")

        screen = self.app.primaryScreen().geometry()
        largura = int(screen.width() * 0.6)
        altura = int(screen.height() * 0.7)

        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone"])

        self.tabela.setAlternatingRowColors(True)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSortingEnabled(True)
        self.tabela.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.tabela)

        botao_atualizar = QPushButton("Atualizar Tabela")
        botao_editar = QPushButton("Editar contato")
        botao_excluir = QPushButton("Excluir contato")
        
        botao_excluir.setStyleSheet("background-color: #e74c3c;") 

        self.layout.addWidget(botao_atualizar)
        self.layout.addWidget(botao_editar)
        self.layout.addWidget(botao_excluir)

        botao_atualizar.clicked.connect(self.carregar_dados)
        botao_excluir.clicked.connect(self.deletar_contato)
        botao_editar.clicked.connect(self.editar_contato)
        self.botao_voltar = QPushButton("Voltar ao Menu")
        self.botao_voltar.setStyleSheet("background-color: #4b5563;") 
        self.layout.addWidget(self.botao_voltar)

        self.botao_voltar.clicked.connect(self.callback_voltar)

    def carregar_dados(self):
        self.banco.connect()
        contatos = Contatos.listar(self.banco)
        self.banco.disconnect()

        if not contatos:
            self.tabela.setRowCount(0)
            return

        self.tabela.setRowCount(len(contatos))

        for linha, contato in enumerate(contatos):
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(contato["id"])))
            self.tabela.setItem(linha, 1, QTableWidgetItem(contato["nome"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(contato["email"]))
            self.tabela.setItem(linha, 3, QTableWidgetItem(contato["telefone"]))
            
    def deletar_contato(self):
        linha_selecionada = self.tabela.currentRow()
        
        if linha_selecionada == -1:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um contato na tabela primeiro!")
            return

        id_contato = self.tabela.item(linha_selecionada, 0).text()

        resposta = QMessageBox.question(
            self.janela, 
            "Confirmar Exclusão", 
            "Tem certeza que deseja excluir este contato?", 
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            self.banco.connect()
            try:
                Contatos.excluir(id_contato, self.banco)
                QMessageBox.information(self.janela, "Sucesso", "Contato excluído com sucesso!")
                self.carregar_dados() 
            except Exception as e:
                QMessageBox.critical(self.janela, "Erro", f"Erro ao excluir: {e}")
            finally:
                self.banco.disconnect()
                
    def editar_contato(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um contato na tabela para editar!")
            return

        id_contato = self.tabela.item(linha_selecionada, 0).text()
        nome = self.tabela.item(linha_selecionada, 1).text()
        email = self.tabela.item(linha_selecionada, 2).text()
        telefone = self.tabela.item(linha_selecionada, 3).text()

        self.tela_edicao = Editar(self.app, id_contato, nome, email, telefone, self)
        self.tela_edicao.janela.show()