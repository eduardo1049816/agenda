from modules.mysql import MySQL
from modules.contatos import Contatos

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
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

        # ===== ESTILO DA TELA MODO ESCURO =====
        self.janela.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: Arial;
                font-size: 14px;
            }

            QLabel {
                color: #e5e7eb; /* Cinza bem claro para o texto */
                font-weight: bold;
                margin-top: 8px;
            }

            QLineEdit {
                background-color: #1f2937; /* Cinza um pouco mais claro para a caixa de texto */
                color: #ffffff; /* Letra digitada branca */
                border: 1px solid #374151; /* Borda sutil */
                border-radius: 6px;
                padding: 8px;
            }

            QLineEdit:focus {
                border: 2px solid #3b82f6; /* Borda azul ao clicar */
                background-color: #27323f;
            }

            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 10px;
                padding: 12px;
                margin-top: 15px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
        """)
        # ====================================

        # Ajustes visuais (não alteram estrutura)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.janela.setWindowTitle("Cadastrar Contato")

        # 🔹 Redimensiona dinamicamente com base na tela
        tela = QGuiApplication.primaryScreen().availableGeometry()
        largura = int(tela.width() * 0.4)
        altura = int(tela.height() * 0.6)

        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        componentes = {
            "nome": "Digite seu nome:",
            "email": "Digite seu email:",
            "telefone": "Digite seu telefone:"
        }

        for chave, valor in componentes.items():
            label = QLabel(valor)
            campo = QLineEdit()

            self.layout.addWidget(label)
            self.layout.addWidget(campo)

            self.campos[chave] = campo

        self.botao_Cadastrar = QPushButton("Cadastrar")
        self.layout.addWidget(self.botao_Cadastrar)
        self.botao_Cadastrar.clicked.connect(self.cadastrar)
        self.botao_voltar = QPushButton("Voltar ao Menu")
        self.botao_voltar.setStyleSheet("background-color: #4b5563;") 
        self.layout.addWidget(self.botao_voltar)

        self.botao_voltar.clicked.connect(self.callback_voltar)

    def validar_campos(self):
        for chave, campo in self.campos.items():
            if not campo.text().strip():
                QMessageBox.warning(
                    self.janela,
                    "Validação",
                    f"O campo '{chave}' é obrigatório."
                )
                campo.setFocus()
                return False

        if "@" not in self.campos["email"].text():
            QMessageBox.warning(
                self.janela,
                "Validação",
                "Email inválido."
            )
            self.campos["email"].setFocus()
            return False
        return True

    def cadastrar(self):
        if not self.validar_campos():
            return

        contatos = Contatos(
            self.campos['nome'].text(),
            self.campos['email'].text(),
            self.campos['telefone'].text()
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

    tela = Cadastrar(app)
    tela.janela.show()

    sys.exit(app.exec())