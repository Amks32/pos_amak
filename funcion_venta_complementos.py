from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt
from conexion import obtener_clientes
from funciones_guardado import guardar_historial_venta, guardar_detalles_venta

class NitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Ingresar NIT")

        layout = QVBoxLayout(self)

        self.nit_label = QLabel("Ingresar NIT:")
        self.nit_input = QLineEdit()
        layout.addWidget(self.nit_label)
        layout.addWidget(self.nit_input)

        self.re_nit_label = QLabel("Redigitar NIT:")
        self.re_nit_input = QLineEdit()
        layout.addWidget(self.re_nit_label)
        layout.addWidget(self.re_nit_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.verify_nit)
        layout.addWidget(self.submit_button)

    def verify_nit(self):
        nit = self.nit_input.text()
        re_nit = self.re_nit_input.text()

        if nit != re_nit:
            QMessageBox.warning(self, "Error", "Los NITs no coinciden.")
        else:
            self.accept()
            self.parent.buscar_cliente_por_nit(nit)

    def get_nit(self):
        return self.nit_input.text()

class VentasComplementos:
    def __init__(self, main_window):
        self.main_window = main_window
        self.inicializar_campos_cliente()

    def inicializar_campos_cliente(self):
        """Inicializa los campos del cliente con los valores de la primera fila de la tabla clientes."""
        clientes = obtener_clientes()
        if clientes:
            primer_cliente = clientes[0]
            self.actualizar_datos_cliente(primer_cliente)

    def actualizar_datos_cliente(self, cliente):
        self.main_window.cliente_fields["Nombre"].setText(str(cliente['nombre']))
        self.main_window.cliente_fields["NIT"].setText(str(cliente['nit_cliente']))
        self.main_window.cliente_fields["ID Cliente"].setText(str(cliente['id_cliente']))
        self.main_window.cliente_fields["Estado"].setText(str(cliente['categoria_cliente']))
        self.main_window.cliente_fields["Dirección"].setText(str(cliente['direccion']))
        self.main_window.cliente_fields["Identificación"].setText(str(cliente['identificacion']))
        self.main_window.cliente_fields["Puntos"].setText(str(cliente['columna_extra_1']))

        # Calcular la conversión en descuento
        try:
            puntos_acumulados = int(cliente['columna_extra_1']) if cliente['columna_extra_1'] is not None else 0
        except ValueError:
            puntos_acumulados = 0

        if puntos_acumulados > 0:
            conversion_descuento = puntos_acumulados / 50
        else:
            conversion_descuento = 0
        self.main_window.cliente_fields["Promoción"].setText(f"{conversion_descuento:.2f}")

    def buscar_cliente_por_nit(self, nit):
        """Busca un cliente por NIT y actualiza los campos si se encuentra una coincidencia."""
        clientes = obtener_clientes()
        cliente_encontrado = next((c for c in clientes if str(c['nit_cliente']) == nit), None)
        if cliente_encontrado:
            print("Cliente encontrado:", cliente_encontrado)  # Debugging line
            self.actualizar_datos_cliente(cliente_encontrado)
        else:
            QMessageBox.warning(self.main_window, "Error", f"No se encontró un cliente con el NIT: {nit}")

    def show_payment_dialog(self, usuario_actual):
        """Muestra el diálogo de método de pago."""
        if self.main_window.iniciar_sesion_action.isEnabled():
            return

        total_text = self.main_window.venta_fields["TOTAL"].text()
        if not total_text or float(total_text) == 0.0:
            QMessageBox.warning(self.main_window, "Error", "Debe realizar una venta primero.")
            return

        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Método de Pago")

        layout = QVBoxLayout(dialog)

        # Barra TOTAL
        total_label = QLabel("TOTAL:")
        total_value = QLineEdit()
        total_value.setReadOnly(True)
        total_value.setText(total_text)
        layout.addWidget(total_label)
        layout.addWidget(total_value)

        # Barra Efectivo
        efectivo_label = QLabel("Efectivo:")
        self.efectivo_value = QLineEdit()
        self.efectivo_value.textChanged.connect(self.update_payment_sum)
        layout.addWidget(efectivo_label)
        layout.addWidget(self.efectivo_value)

        # Barra Tarjeta
        tarjeta_label = QLabel("Tarjeta:")
        self.tarjeta_value = QLineEdit()
        self.tarjeta_value.textChanged.connect(self.update_payment_sum)
        layout.addWidget(tarjeta_label)
        layout.addWidget(self.tarjeta_value)

        # Barra Otros
        otros_label = QLabel("Otros:")
        self.otros_value = QLineEdit()
        self.otros_value.textChanged.connect(self.update_payment_sum)
        layout.addWidget(otros_label)
        layout.addWidget(self.otros_value)

        # Barra Suma Total
        suma_label = QLabel("Suma Total:")
        self.suma_value = QLineEdit()
        self.suma_value.setReadOnly(True)
        layout.addWidget(suma_label)
        layout.addWidget(self.suma_value)

        # Botón de Aceptar
        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(lambda: self.verify_payment(dialog))
        layout.addWidget(accept_button)

        dialog.setLayout(layout)
        dialog.exec()

    def update_payment_sum(self):
        """Actualiza la suma total de los métodos de pago."""
        try:
            efectivo = float(self.efectivo_value.text()) if self.efectivo_value.text() else 0.0
            tarjeta = float(self.tarjeta_value.text()) if self.tarjeta_value.text() else 0.0
            otros = float(self.otros_value.text()) if self.otros_value.text() else 0.0
            suma_total = efectivo + tarjeta + otros
            self.suma_value.setText(f"{suma_total:.2f}")
        except ValueError:
            self.suma_value.setText("0.00")

    def verify_payment(self, dialog):
        """Verifica si la suma de los métodos de pago es mayor o igual a TOTAL."""
        total_text = self.main_window.venta_fields["TOTAL"].text()
        suma_total_text = self.suma_value.text()

        if not suma_total_text or float(suma_total_text) < float(total_text):
            QMessageBox.warning(self.main_window, "Error", "Faltan CAMELLOS.")
            return

        total = float(total_text)
        suma_total = float(suma_total_text)

        if suma_total >= total:
            cambio = suma_total - total
            QMessageBox.information(self.main_window, "Éxito", f"Venta realizada con éxito. El cambio es de: {cambio:.2f}")
            self.guardar_venta()
            dialog.accept()

    def guardar_venta(self):
        """Guarda la venta en la base de datos."""
        id_cliente = int(self.main_window.cliente_fields["ID Cliente"].text())
        usuario = self.main_window.usuario_actual
        total = float(self.main_window.venta_fields["TOTAL"].text())
        efectivo = float(self.efectivo_value.text()) if self.efectivo_value.text() else 0.0
        tarjeta = float(self.tarjeta_value.text()) if self.tarjeta_value.text() else 0.0
        otros = float(self.otros_value.text()) if self.otros_value.text() else 0.0

        id_venta = guardar_historial_venta(id_cliente, usuario, total, efectivo, tarjeta, otros)
        if id_venta:
            resultado = guardar_detalles_venta(id_venta, self.main_window.table)
            if resultado:
                print("Detalles de venta guardados con éxito.")
            else:
                print("Error al guardar los detalles de venta.")
        else:
            print("Error al guardar el historial de venta.")