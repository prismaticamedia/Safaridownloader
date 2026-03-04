#!/usr/bin/env python3
import sys
import json
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QCheckBox, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, book_id, pdf):
        super().__init__()
        self.book_id = book_id
        self.pdf = pdf

    def run(self):
        cmd = ["python3", "s4f4ridownload.py", self.book_id]
        if self.pdf:
            cmd.insert(2, "--pdf")

        try:
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env, cwd=script_dir)
            for line in iter(self.process.stdout.readline, ''):
                self.output_signal.emit(line)
            self.process.stdout.close()
            self.process.wait()
            self.output_signal.emit(f"\\nProcess finished with exit code {self.process.returncode}\\n")
            self.finished_signal.emit(self.process.returncode)
        except Exception as e:
            self.output_signal.emit(f"\\nError running script: {e}\\n")
            self.finished_signal.emit(-1)

    def cancel(self):
        if hasattr(self, 'process') and self.process:
            self.process.terminate()
            self.output_signal.emit("\\nProcess cancelled by user.\\n")

class S4f4riDownloadUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S4f4riDownload (PyQt6)")
        self.resize(750, 550)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.setup_cookies_tab()
        self.setup_download_tab()

    def setup_cookies_tab(self):
        self.tab_cookies = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Paste your cookies.json content here (or raw Netscape cookies format if supported):")
        layout.addWidget(label)

        self.cookies_text = QTextEdit()
        layout.addWidget(self.cookies_text)

        if os.path.exists("cookies.json"):
            try:
                with open("cookies.json", "r") as f:
                    self.cookies_text.setText(f.read())
            except Exception:
                pass

        self.save_btn = QPushButton("Save cookies.json")
        self.save_btn.clicked.connect(self.save_cookies)
        
        self.clear_btn = QPushButton("Clear cookies.json")
        self.clear_btn.clicked.connect(self.clear_cookies)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

        self.tab_cookies.setLayout(layout)
        self.tabs.addTab(self.tab_cookies, "1. Paste Cookies")

    def setup_download_tab(self):
        self.tab_download = QWidget()
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Book ID or URL:"))
        
        self.book_id_input = QLineEdit()
        self.book_id_input.setPlaceholderText("e.g. 9781835880401 or full URL")
        input_layout.addWidget(self.book_id_input)

        self.pdf_check = QCheckBox("Generate PDF (Books only)")
        self.pdf_check.setChecked(True)
        input_layout.addWidget(self.pdf_check)

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        input_layout.addWidget(self.download_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        input_layout.addWidget(self.cancel_btn)

        layout.addLayout(input_layout)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        # set dark theme for console
        self.output_console.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: monospace; font-size: 13px;")
        layout.addWidget(self.output_console)

        self.tab_download.setLayout(layout)
        self.tabs.addTab(self.tab_download, "2. Download Book")

    def save_cookies(self):
        content = self.cookies_text.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "Input Error", "Please paste your cookies.")
            return

        try:
            parsed = json.loads(content)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cookies_file = os.path.join(script_dir, "cookies.json")
            with open(cookies_file, "w") as f:
                json.dump(parsed, f, indent=4)
            QMessageBox.information(self, "Success", "cookies.json saved successfully!\\n\\nYou can now go to the Download tab.")
            self.tabs.setCurrentIndex(1)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON Error", f"Invalid JSON format.\\n\\nError: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save cookies.json.\\n\\nError: {e}")

    def start_download(self):
        book_input = self.book_id_input.text().strip()
        if not book_input:
            QMessageBox.warning(self, "Input Error", "Please enter a Book ID or URL.")
            return

        book_id = book_input.strip('/').split('/')[-1]
        
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.output_console.clear()
        self.output_console.append(f"Starting download for Book ID: {book_id}\\n")

        self.thread = DownloadThread(book_id, self.pdf_check.isChecked())
        self.thread.output_signal.connect(self.append_output)
        self.thread.finished_signal.connect(self.download_finished)
        self.thread.start()

    def append_output(self, text):
        self.output_console.insertPlainText(text)
        self.output_console.ensureCursorVisible()

    def cancel_download(self):
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.cancel()
            self.cancel_btn.setEnabled(False)
            self.download_btn.setEnabled(True)

    def clear_cookies(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cookies_file = os.path.join(script_dir, "cookies.json")
            if os.path.exists(cookies_file):
                os.remove(cookies_file)
            self.cookies_text.clear()
            QMessageBox.information(self, "Success", "cookies.json cleared successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to clear cookies.json.\\n\\nError: {e}")

    def download_finished(self, exit_code):
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        if exit_code == 0:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            books_dir = os.path.join(script_dir, "Books")
            if os.path.exists(books_dir):
                subprocess.run(['open', books_dir])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = S4f4riDownloadUI()
    window.show()
    sys.exit(app.exec())
