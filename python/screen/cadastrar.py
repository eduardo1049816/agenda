from modules.mysql import MySQL
from modules.contatos import Contatos

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QGuiApplication


class Cadastrar:
    def __init__(self, app, callback_voltar):
        self.app = app
        self.callback_voltar = callback_voltar
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        self.campos = {}

        self.janela.setStyleSheet("""
            QWidget { background-color: #121212; font-family: Arial; font-size: 14px; }
            QLabel { color: #e5e7eb; font-weight: bold; margin-top: 8px; }
            QLineEdit { background-color: #1f2937; color: #ffffff; border: 1px solid #374151; border-radius: 6px; padding: 8px; }
            QLineEdit:focus { border: 2px solid #3b82f6; background-color: #27323f; }
        """)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.janela.setWindowTitle("Cadastrar Contato")
        tela = QGuiApplication.primaryScreen().availableGeometry()
        largura = int(tela.width() * 0.4)
        altura = int(tela.height() * 0.6)
        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        componentes = {
            "nome": "Nome:",
            "email": "E-mail:",
            "telefone": "Celular:"
        }

        for chave, valor in componentes.items():
            label = QLabel(valor)
            campo = QLineEdit()
            self.layout.addWidget(label)
            self.layout.addWidget(campo)
            self.campos[chave] = campo


        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15)

        self.botao_cadastrar = QPushButton("Cadastrar")
        self.botao_voltar = QPushButton("Voltar ao Menu")

        estilo_botoes = "QPushButton { color: white; border-radius: 8px; padding: 12px; font-size: 15px; font-weight: bold; margin-top: 15px; }"
        
        self.botao_cadastrar.setStyleSheet(estilo_botoes + "QPushButton { background-color: #10b981; } QPushButton:hover { background-color: #059669; }")
        self.botao_voltar.setStyleSheet(estilo_botoes + "QPushButton { background-color: #4b5563; } QPushButton:hover { background-color: #374151; }")

        for botao in [self.botao_cadastrar, self.botao_voltar]:
            botao.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout_botoes.addWidget(botao)

        self.layout.addLayout(layout_botoes)


        self.botao_cadastrar.clicked.connect(self.cadastrar)
        self.botao_voltar.clicked.connect(self.callback_voltar)

    def validar_campos(self):
        for chave, campo in self.campos.items():
            if not campo.text().strip():
                QMessageBox.warning(self.janela, "Validação", f"O campo '{chave}' é obrigatório.")
                campo.setFocus()
                return False

        if "@" not in self.campos["email"].text():
            QMessageBox.warning(self.janela, "Validação", "Email inválido.")
            self.campos["email"].setFocus()
            return False
        return True

    def cadastrar(self):
        if not self.validar_campos():
            return


        contatos = Contatos(
            self.campos['nome'].text().strip().title(),
            self.campos['email'].text().strip().lower(),
            self.campos['telefone'].text().strip()
        )

        self.banco.connect()
        try:
            contatos.cadastrar(self.banco)
            QMessageBox.information(self.janela, "Sucesso", "Contato cadastrado!")
            self.limpar_campos()
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Erro ao cadastrar: {str(e)}")
        finally:
            self.banco.disconnect()

    def limpar_campos(self):
        for campo in self.campos.values():
            campo.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Cadastrar(app, lambda: print("Voltar ao menu chamado"))
    tela.janela.show()
    sys.exit(app.exec())