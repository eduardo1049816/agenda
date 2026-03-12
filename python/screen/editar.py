from modules.mysql import MySQL
from modules.contatos import Contatos

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PySide6.QtGui import QGuiApplication

class Editar:
    def __init__(self, app, id_contato, nome, email, telefone, tela_listagem):
        self.app = app
        self.id_contato = id_contato
        self.nome_atual = nome
        self.email_atual = email
        self.telefone_atual = telefone
        self.tela_listagem = tela_listagem 
        
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        self.campos = {}

        self.janela.setStyleSheet("""
            QWidget { background-color: #121212; font-family: Arial; font-size: 14px; }
            QLabel { color: #e5e7eb; font-weight: bold; margin-top: 8px; }
            QLineEdit { background-color: #1f2937; color: #ffffff; border: 1px solid #374151; border-radius: 6px; padding: 8px; }
            QLineEdit:focus { border: 2px solid #3b82f6; background-color: #27323f; }
            QPushButton {
                background-color: #10b981; /* Verde para confirmar a edição */
                color: white; border-radius: 10px; padding: 12px; margin-top: 15px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
        """)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.janela.setWindowTitle(f"Editar Contato - ID: {self.id_contato}")

        tela = QGuiApplication.primaryScreen().availableGeometry()
        largura = int(tela.width() * 0.4)
        altura = int(tela.height() * 0.6)

        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        componentes = {
            "nome": ("Nome:", self.nome_atual),
            "email": ("Email:", self.email_atual),
            "telefone": ("Telefone:", self.telefone_atual)
        }

        for chave, (texto_label, valor_atual) in componentes.items():
            label = QLabel(texto_label)
            campo = QLineEdit()
            campo.setText(valor_atual) 

            self.layout.addWidget(label)
            self.layout.addWidget(campo)

            self.campos[chave] = campo

        self.botao_salvar = QPushButton("Salvar Alterações")
        self.layout.addWidget(self.botao_salvar)
        self.botao_salvar.clicked.connect(self.salvar_edicao)

    def salvar_edicao(self):

        nome = self.campos['nome'].text().strip().title()
        email = self.campos['email'].text().strip().lower()
        telefone = self.campos['telefone'].text().strip()

        if not nome or not email or not telefone:
            QMessageBox.warning(self.janela, "Aviso", "Todos os campos são obrigatórios.")
            return

        self.banco.connect()

        try:
            Contatos.editar(self.id_contato, nome, email, telefone, self.banco)
            QMessageBox.information(self.janela, "Sucesso", "Contato atualizado com sucesso!")
            
            self.tela_listagem.carregar_dados() 
            
            self.janela.close() 
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Erro ao editar: {str(e)}")
        finally:
            self.banco.disconnect()