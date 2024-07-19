import sys
import pyshorteners
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QClipboard, QPalette, QColor

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.resize(800, 600)  # Aumentar o tamanho da janela
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Layout para entrada e resultado
        input_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        
        # Campo de entrada para URL original
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter the URL to shorten")
        self.url_input.setMinimumHeight(40)  # Aumentar a altura da entrada de URL
        self.url_input.setStyleSheet("background-color: #f0f0f0;")
        input_layout.addWidget(QLabel("Original URL:"))
        input_layout.addWidget(self.url_input)
        
        # Botão para encurtar URL
        shorten_button = QPushButton("Shorten", self)
        shorten_button.clicked.connect(self.shorten_url)
        shorten_button.setMinimumHeight(40)  # Ajustar a altura do botão
        input_layout.addWidget(shorten_button)
        
        # Campo de saída para URL encurtado
        self.short_url_output = QLineEdit(self)
        self.short_url_output.setReadOnly(True)
        self.short_url_output.setMinimumHeight(40)  # Aumentar a altura da saída de URL
        self.short_url_output.setStyleSheet("background-color: #f0f0f0;")
        result_layout.addWidget(QLabel("Shortened URL:"))
        result_layout.addWidget(self.short_url_output)
        
        # Botão para copiar URL encurtado
        copy_button = QPushButton("Copy", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setMinimumHeight(40)  # Ajustar a altura do botão
        result_layout.addWidget(copy_button)
        
        # Tabela para histórico
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Original URL", "Shortened URL"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 400)  # Ajustar largura das colunas
        self.history_table.setColumnWidth(1, 400)
        
        # Adicionar layouts ao layout principal
        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addWidget(QLabel("History:"))
        layout.addWidget(self.history_table)
        
        # Configurar layout principal
        self.setLayout(layout)
        
    def shorten_url(self):
        long_url = self.url_input.text()
        short_url = self.get_short_url(long_url)
        self.short_url_output.setText(short_url)
        
        # Atualizar histórico
        row_position = self.history_table.rowCount()
        self.history_table.insertRow(row_position)
        self.history_table.setItem(row_position, 0, QTableWidgetItem(long_url))
        self.history_table.setItem(row_position, 1, QTableWidgetItem(short_url))
        
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
        
def main():
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
