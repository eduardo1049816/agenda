from modules.mysql import MySQL
from modules.contatos import Contatos
from screen.editar import Editar

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,       
    QSizePolicy,       
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

class Listar:
    
    def __init__(self, app, callback_voltar, callback_cadastrar):
        self.app = app
        self.callback_voltar = callback_voltar
        self.callback_cadastrar = callback_cadastrar
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        self.janela.setStyleSheet("""
            QWidget { background-color: #121212; font-family: Arial; font-size: 13px; color: #e5e7eb; }
            QTableWidget {
                background-color: #1f2937; color: #ffffff; border: 1px solid #374151; gridline-color: #374151;
                selection-background-color: #3b82f6; selection-color: white; alternate-background-color: #18202b;
            }
            QHeaderView::section { background-color: #111827; color: #9ca3af; padding: 8px; border: 1px solid #374151; font-weight: bold; }
            QTableWidget::item { padding: 6px; }
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

        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15) 

        botao_novo = QPushButton("Novo Contato") 
        botao_atualizar = QPushButton("Atualizar Tabela")
        botao_editar = QPushButton("Editar Contato")
        botao_excluir = QPushButton("Excluir Contato")
        self.botao_voltar = QPushButton("Voltar ao Menu")

        estilo_base = "QPushButton { color: white; border-radius: 8px; padding: 10px; font-size: 14px; font-weight: bold; margin-top: 10px; }"
        
        botao_novo.setStyleSheet(estilo_base + "QPushButton { background-color: #8b5cf6; } QPushButton:hover { background-color: #7c3aed; }")
        botao_atualizar.setStyleSheet(estilo_base + "QPushButton { background-color: #3b82f6; } QPushButton:hover { background-color: #2563eb; }")
        botao_editar.setStyleSheet(estilo_base + "QPushButton { background-color: #10b981; } QPushButton:hover { background-color: #059669; }")
        botao_excluir.setStyleSheet(estilo_base + "QPushButton { background-color: #ef4444; } QPushButton:hover { background-color: #dc2626; }")
        self.botao_voltar.setStyleSheet(estilo_base + "QPushButton { background-color: #4b5563; } QPushButton:hover { background-color: #374151; }")

        for botao in [botao_novo, botao_atualizar, botao_editar, botao_excluir, self.botao_voltar]:
            botao.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout_botoes.addWidget(botao)

        self.layout.addLayout(layout_botoes)

        botao_novo.clicked.connect(self.callback_cadastrar) 
        botao_atualizar.clicked.connect(self.carregar_dados)
        botao_excluir.clicked.connect(self.deletar_contato)
        botao_editar.clicked.connect(self.editar_contato)
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