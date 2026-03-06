from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QPushButton,
    QWidget
)

from screen.cadastrar import Cadastrar
from screen.listar import Listar

import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # ===== ESTILO GLOBAL DO SISTEMA =====
        self.app.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Arial;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2e86de;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }

            QPushButton:hover {
                background-color: #1b4f72;
            }

            QPushButton:pressed {
                background-color: #154360;
            }
        """)
        

        self.janela = QWidget()
        self.layout = QVBoxLayout()

        # Ajustes visuais (não alteram estrutura)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.janela.setWindowTitle("Agenda")
        self.janela.resize(400, 200)
        self.janela.setLayout(self.layout)

        self.criar_botoes()
        self.janela.show()

    def criar_botoes(self):
        botao_listar = QPushButton("Listar")
        self.layout.addWidget(botao_listar)
        botao_listar.clicked.connect(self.abrir_listagem)

        botao_cadastrar = QPushButton("Cadastrar")
        self.layout.addWidget(botao_cadastrar)
        botao_cadastrar.clicked.connect(self.abrir_cadastro)

    def abrir_listagem(self):
        self.tela_listagem = Listar(self.app)
        self.tela_listagem.janela.show()

    def abrir_cadastro(self):
        self.tela_cadastro = Cadastrar(self.app)
        self.tela_cadastro.janela.show()

if __name__ == "__main__":
    system = App()
    sys.exit(system.app.exec())