from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import QThread, Signal
from mysql.connector import Error
from conexion import obtener_conexion

class LoginThread(QThread):
    result_ready = Signal(object)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        connection = obtener_conexion()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
                cursor.execute(query, (self.username, self.password))
                user = cursor.fetchone()
                self.result_ready.emit(user)
            except Error as e:
                self.result_ready.emit(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setFixedSize(300, 200)
        self.username = None

        layout = QVBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nombre de usuario")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Iniciar Sesión", self)
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")
            return

        print(f"Intentando iniciar sesión con usuario: {username}")
        self.login_thread = LoginThread(username, password)
        self.login_thread.result_ready.connect(self.process_result)
        self.login_thread.start()

    def process_result(self, result):
        if isinstance(result, dict):
            if result['estado'] != 'activo':
                print("Usuario inactivo")
                QMessageBox.warning(self, "Error", "El usuario está inactivo")
            elif result['rol'] not in [1, 2]:
                print("Rol no permitido")
                QMessageBox.warning(self, "Error", "El rol del usuario no está permitido")
            else:
                print("Usuario encontrado en la base de datos")
                self.username = result['nombre_usuario']
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
                self.accept()
        elif isinstance(result, str) and result.startswith("Error:"):
            print(result)
            QMessageBox.critical(self, "Error", result)
        else:
            print("Nombre de usuario o contraseña incorrectos")
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")