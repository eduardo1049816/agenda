from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QPushButton, QWidget, QStackedWidget
)
from screen.cadastrar import Cadastrar
from screen.listar import Listar
import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.app.setStyleSheet("""
            QWidget { background-color: #121212; font-family: Arial; font-size: 14px; }
            QPushButton {
                background-color: #3b82f6; color: white; border-radius: 10px;
                padding: 15px; font-size: 16px; font-weight: bold; margin: 10px;
            }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
        """)

        self.janela_principal = QWidget()
        self.janela_principal.setWindowTitle("Agenda de Contatos")
        self.janela_principal.resize(800, 600) 
        
        self.layout_principal = QVBoxLayout(self.janela_principal)
        self.layout_principal.setContentsMargins(0, 0, 0, 0) 

        self.stack = QStackedWidget()
        self.layout_principal.addWidget(self.stack)

        self.tela_menu = QWidget()
        self.layout_menu = QVBoxLayout(self.tela_menu)
        self.layout_menu.setSpacing(15)
        self.layout_menu.setContentsMargins(50, 50, 50, 50)

        botao_listar = QPushButton("Ver Contatos")
        botao_cadastrar = QPushButton("Novo Contato")

        self.layout_menu.addWidget(botao_listar)
        self.layout_menu.addWidget(botao_cadastrar)

        self.tela_listagem = Listar(self.app, self.mostrar_menu)
        self.tela_cadastro = Cadastrar(self.app, self.mostrar_menu)

        self.stack.addWidget(self.tela_menu)              
        self.stack.addWidget(self.tela_listagem.janela)   
        self.stack.addWidget(self.tela_cadastro.janela)   

        botao_listar.clicked.connect(self.mostrar_listagem)
        botao_cadastrar.clicked.connect(self.mostrar_cadastro)

        self.janela_principal.show()

    def mostrar_menu(self):
        self.stack.setCurrentIndex(0) 

    def mostrar_listagem(self):
        try:
            self.tela_listagem.carregar_dados()
        except: pass
        self.stack.setCurrentIndex(1) 

    def mostrar_cadastro(self):
        self.stack.setCurrentIndex(2) 


if __name__ == "__main__":
    system = App()
    sys.exit(system.app.exec())