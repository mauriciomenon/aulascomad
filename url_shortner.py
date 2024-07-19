import sys
import pyshorteners
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QClipboard

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('URL Shortener')
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Layout para entrada e resultado
        input_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        
        # Campo de entrada para URL original
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter the URL to shorten")
        input_layout.addWidget(QLabel("Original URL:"))
        input_layout.addWidget(self.url_input)
        
        # Campo de saída para URL encurtado
        self.short_url_output = QLineEdit(self)
        self.short_url_output.setReadOnly(True)
        result_layout.addWidget(QLabel("Shortened URL:"))
        result_layout.addWidget(self.short_url_output)
        
        # Botão para encurtar URL
        shorten_button = QPushButton("Shorten", self)
        shorten_button.clicked.connect(self.shorten_url)
        input_layout.addWidget(shorten_button)
        
        # Botão para copiar URL encurtado
        copy_button = QPushButton("Copy", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        result_layout.addWidget(copy_button)
        
        # Área de texto para histórico
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        
        # Adicionar layouts ao layout principal
        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addWidget(QLabel("History:"))
        layout.addWidget(self.history_text)
        
        # Configurar layout principal
        self.setLayout(layout)
        
    def shorten_url(self):
        long_url = self.url_input.text()
        short_url = self.get_short_url(long_url)
        self.short_url_output.setText(short_url)
        
        # Atualizar histórico
        self.history_text.append(f"Original: {long_url}\nShortened: {short_url}\n")
        
    def get_short_url(self, long_url):
        try:
            type_tiny = pyshorteners.Shortener(timeout=10)
            short_url = type_tiny.tinyurl.short(long_url)
            return short_url
        except Exception as e:
            return f"Error: {e}"
        
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.short_url_output.text())
        self.history_text.append("Shortened URL copied to clipboard.\n")

def main():
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
