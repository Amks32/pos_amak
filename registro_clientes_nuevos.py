#registro_clientes_nuevos.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import QDate
from conexion import obtener_clientes, registrar_cliente
import re

class RegistroClientesNuevos(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nuevo Cliente")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Obtener el último ID de cliente
        clientes = obtener_clientes()
        if clientes:
            ultimo_id = max(cliente['id_cliente'] for cliente in clientes)
            nuevo_id = ultimo_id + 1
        else:
            nuevo_id = 1

        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit(str(nuevo_id))
        self.id_input.setReadOnly(True)
        form_layout.addRow(self.id_label, self.id_input)

        self.nit_label = QLabel("NIT Cliente:")
        self.nit_input = QLineEdit()
        form_layout.addRow(self.nit_label, self.nit_input)

        self.identificacion_label = QLabel("Identificación:")
        self.identificacion_input = QLineEdit()
        form_layout.addRow(self.identificacion_label, self.identificacion_input)

        self.nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        form_layout.addRow(self.nombre_label, self.nombre_input)

        self.gmail_label = QLabel("Gmail:")
        self.gmail_input = QLineEdit()
        form_layout.addRow(self.gmail_label, self.gmail_input)

        self.telefono_label = QLabel("Teléfono:")
        self.telefono_input = QLineEdit()
        form_layout.addRow(self.telefono_label, self.telefono_input)

        self.direccion_label = QLabel("Dirección:")
        self.direccion_input = QLineEdit()
        form_layout.addRow(self.direccion_label, self.direccion_input)

        self.fecha_registro_label = QLabel("Fecha de Registro:")
        self.fecha_registro_input = QLineEdit(QDate.currentDate().toString("yyyy-MM-dd"))
        self.fecha_registro_input.setReadOnly(True)
        form_layout.addRow(self.fecha_registro_label, self.fecha_registro_input)

        self.fecha_nacimiento_label = QLabel("Fecha de Nacimiento:")
        self.fecha_nacimiento_input = QLineEdit()
        form_layout.addRow(self.fecha_nacimiento_label, self.fecha_nacimiento_input)

        self.sexo_label = QLabel("Sexo:")
        self.sexo_input = QLineEdit()
        form_layout.addRow(self.sexo_label, self.sexo_input)

        self.submit_button = QPushButton("Registrar")
        self.submit_button.clicked.connect(self.registrar_cliente)
        form_layout.addRow(self.submit_button)

        layout.addLayout(form_layout)

    def registrar_cliente(self):
        cliente = {
            'id_cliente': int(self.id_input.text()),
            'nit_cliente': self.nit_input.text(),
            'identificacion': self.identificacion_input.text(),
            'nombre': self.nombre_input.text(),
            'gmail': self.gmail_input.text(),
            'telefono': self.telefono_input.text(),
            'direccion': self.direccion_input.text(),
            'fecha_registro': self.fecha_registro_input.text(),
            'fecha_nacimiento': self.fecha_nacimiento_input.text(),
            'sexo': self.sexo_input.text(),
            'categoria_cliente': '',  # Campo vacío
            'notas': '',  # Campo vacío
        }

        # Verificar que los campos imprescindibles no estén vacíos
        if not cliente['nit_cliente']:
            QMessageBox.warning(self, "Error", "El campo 'NIT Cliente' es obligatorio.")
            return
        if not cliente['nombre']:
            QMessageBox.warning(self, "Error", "El campo 'Nombre' es obligatorio.")
            return
        if not cliente['telefono']:
            QMessageBox.warning(self, "Error", "El campo 'Teléfono' es obligatorio.")
            return
        if not cliente['direccion']:
            QMessageBox.warning(self, "Error", "El campo 'Dirección' es obligatorio.")
            return
        if not cliente['fecha_nacimiento']:
            QMessageBox.warning(self, "Error", "El campo 'Fecha de Nacimiento' es obligatorio.")
            return

        # Verificar formato de fecha de nacimiento
        fecha_nacimiento = QDate.fromString(cliente['fecha_nacimiento'], "yyyy-MM-dd")
        if not fecha_nacimiento.isValid():
            QMessageBox.warning(self, "Error", "El formato de la 'Fecha de Nacimiento' debe ser 'yyyy-MM-dd'.")
            return

        # Verificar que el sexo sea 'M' o 'F'
        if cliente['sexo'] and cliente['sexo'] not in ['M', 'F']:
            QMessageBox.warning(self, "Error", "El campo 'Sexo' debe ser 'M' o 'F'.")
            return

        if registrar_cliente(cliente):
            QMessageBox.information(self, "Éxito", "Cliente registrado exitosamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Hubo un error al registrar el cliente.")