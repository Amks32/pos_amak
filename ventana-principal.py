import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStatusBar, QLabel, QMenuBar, QMenu, QMessageBox,
    QVBoxLayout, QWidget, QDialog, QTableWidget, QTableWidgetItem, QDockWidget,
    QGroupBox, QLineEdit, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QAction, QKeySequence, QColor
from PySide6.QtCore import Qt
from login import LoginDialog
from funcion_venta_complementos import NitDialog, VentasComplementos
from registro_clientes_nuevos import RegistroClientesNuevos
from conexion import obtener_clientes
from funcion_venta import obtener_valor_busqueda, update_total_facturado, obtener_stock, obtener_descuentos  # Importar la función desde funcion_venta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema POS")
        self.usuario_actual = None

        # Barra de estado
        status_bar = QStatusBar()
        status_bar_label = QLabel("Barra de Estado - Aquí puedes mostrar información útil")
        status_bar.addWidget(status_bar_label)
        self.setStatusBar(status_bar)

        # Menú superior
        menu_bar = QMenuBar(self)
        aplicacion_menu = QMenu("Aplicación", self)

        self.iniciar_sesion_action = QAction("Iniciar Sesión", self)
        self.iniciar_sesion_action.triggered.connect(self.show_login_dialog)
        aplicacion_menu.addAction(self.iniciar_sesion_action)

        cerrar_sesion_action = QAction("Cerrar Sesión", self)
        cerrar_sesion_action.triggered.connect(self.close_session)
        aplicacion_menu.addAction(cerrar_sesion_action)

        menu_bar.addMenu(aplicacion_menu)
        menu_bar.addAction(QAction("Reportes", self, triggered=self.show_reports))
        menu_bar.addAction(QAction("Soporte", self, triggered=self.customer_support))
        menu_bar.addAction(QAction("Historial", self, triggered=self.view_sales_history))
        menu_bar.addAction(QAction("Día", self, triggered=self.view_day))

        self.setMenuBar(menu_bar)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)

        # Crear widgets centrales y barras laterales
        self.create_dock_widgets()
        self.create_central_widgets()

        # Atajos de teclado
        self.shortcut_f8 = QAction(self)
        self.shortcut_f8.setShortcut(QKeySequence(Qt.Key_F8))
        self.shortcut_f8.triggered.connect(self.show_nit_dialog)
        self.addAction(self.shortcut_f8)

        self.shortcut_f1 = QAction(self)
        self.shortcut_f1.setShortcut(QKeySequence(Qt.Key_F1))
        self.shortcut_f1.triggered.connect(self.show_payment_dialog)
        self.addAction(self.shortcut_f1)

        self.shortcut_f5 = QAction(self)
        self.shortcut_f5.setShortcut(QKeySequence(Qt.Key_F5))
        self.shortcut_f5.triggered.connect(self.handle_search_nit)
        self.addAction(self.shortcut_f5)

        # Inicialmente ocultar los widgets centrales y las barras laterales
        self.toggle_widgets_visibility(False)

        # Inicializar la lista de productos
        self.productos = []

        # Inicializar los campos del cliente con valores predeterminados
        VentasComplementos(self).inicializar_campos_cliente()

    def show_login_dialog(self):
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            print("Sesión iniciada exitosamente")
            self.usuario_actual = login_dialog.username
            self.iniciar_sesion_action.setEnabled(False)  # Deshabilitar el botón de "Iniciar Sesión"
            self.toggle_widgets_visibility(True)  # Mostrar los widgets centrales y las barras laterales

    def close_session(self):
        print("Sesión cerrada exitosamente")
        QMessageBox.information(self, "Cerrar Sesión", "Sesión cerrada exitosamente")

        # Eliminar dock widgets
        for dock_widget in self.findChildren(QDockWidget):
            dock_widget.setParent(None)
            dock_widget.close()

        # Eliminar widgets centrales
        while self.central_layout.count():
            child = self.central_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.iniciar_sesion_action.setEnabled(True)
        self.usuario_actual = None
        self.toggle_widgets_visibility(False)  # Ocultar los widgets centrales y las barras laterales

    def create_dock_widgets(self):
        """Crea las barras laterales (dock widgets)"""
        # Dock Izquierdo - Activación de Ofertas y Productos
        self.left_dock = QDockWidget("Activación de Ofertas y Productos", self)
        self.left_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.left_dock.setFeatures(QDockWidget.DockWidgetMovable)  # Deshabilitar el cierre

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Grupo de Activación de Ofertas
        ofertas_groupbox = QGroupBox("Activación de Ofertas")
        ofertas_layout = QVBoxLayout(ofertas_groupbox)
        self.ofertas_table = QTableWidget(0, 4)
        self.ofertas_table.setHorizontalHeaderLabels(["Oferta", "Descripción", "Precio", "Fecha de Finalización"])
        ofertas_layout.addWidget(self.ofertas_table)
        left_layout.addWidget(ofertas_groupbox)

        # Grupo de Productos
        productos_groupbox = QGroupBox("Productos")
        productos_layout = QVBoxLayout(productos_groupbox)
        
        # Barra de búsqueda por descripción
        self.productos_search_bar = QLineEdit()
        self.productos_search_bar.setPlaceholderText("Buscar por descripción...")
        self.productos_search_bar.textChanged.connect(self.buscar_por_descripcion)
        productos_layout.addWidget(self.productos_search_bar)
        
        self.productos_table = QTableWidget(0, 3)
        self.productos_table.setHorizontalHeaderLabels(["ID", "Descripción", "Precio"])
        productos_layout.addWidget(self.productos_table)
        left_layout.addWidget(productos_groupbox)

        self.left_dock.setWidget(left_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        # Dock Derecho - Detalles del Cliente
        self.right_dock = QDockWidget("Detalles del Cliente", self)
        self.right_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.right_dock.setFeatures(QDockWidget.DockWidgetMovable)  # Deshabilitar el cierre

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Datos del Cliente
        cliente_groupbox = QGroupBox("Detalles del Cliente")
        cliente_layout = QVBoxLayout(cliente_groupbox)
        labels = ["Nombre", "NIT", "ID Cliente", "Estado", "Dirección", "Identificación", "Puntos", "Promoción"]
        self.cliente_fields = {}
        for label in labels:
            cliente_layout.addWidget(QLabel(label + ":"))
            field = QLineEdit()
            field.setReadOnly(True)
            cliente_layout.addWidget(field)
            self.cliente_fields[label] = field
        right_layout.addWidget(cliente_groupbox)

        # Datos de Venta
        venta_groupbox = QGroupBox("Datos de Venta")
        venta_layout = QVBoxLayout(venta_groupbox)
        labels_venta = ["Total Facturado", "Descuento Promoción", "Descuento Mayorista", "Facturado en Promoción", "TOTAL"]
        self.venta_fields = {}
        for label in labels_venta:
            layout = QHBoxLayout()
            field = QLineEdit()
            field.setReadOnly(True)
            field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout.addWidget(QLabel(label + ":"))
            layout.addWidget(field)
            venta_layout.addLayout(layout)
            self.venta_fields[label] = field
        right_layout.addWidget(venta_groupbox)

        # Puntos del Cliente
        puntos_groupbox = QGroupBox("Puntos del Cliente")
        puntos_layout = QVBoxLayout(puntos_groupbox)
        self.puntos_acumulados = QLineEdit()
        self.puntos_acumulados.setReadOnly(True)
        puntos_layout.addWidget(QLabel("Puntos Acumulados:"))
        puntos_layout.addWidget(self.puntos_acumulados)
        self.conversion_descuento = QLineEdit()
        self.conversion_descuento.setReadOnly(True)
        puntos_layout.addWidget(QLabel("Conversión a Descuento:"))
        puntos_layout.addWidget(self.conversion_descuento)
        right_layout.addWidget(puntos_groupbox)

        right_widget.setLayout(right_layout)
        self.right_dock.setWidget(right_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)

    def create_central_widgets(self):
        """Crea la barra de búsqueda y la tabla principal"""
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Buscar productos...")
        self.search_bar = search_bar
        self.search_bar.returnPressed.connect(self.handle_search)

        table = QTableWidget(0, 8)  # Cambiar el número de columnas a 8
        table.setHorizontalHeaderLabels(["ID", "Descripción", "Precio", "Unidades", "Subtotal", "Descuento", "Promoción", "Mayorista"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        self.table = table

        total_label = QLabel("Total: Q0.00")
        self.total_label = total_label

        layout = QVBoxLayout()
        layout.addWidget(search_bar)
        layout.addWidget(table)
        layout.addWidget(total_label)
        self.central_layout.addLayout(layout)

    def handle_search(self):
        """Maneja la búsqueda de productos"""
        try:
            id_busqueda = obtener_valor_busqueda(self)
            print(f"ID de producto buscado: {id_busqueda}")
            # Aquí puedes agregar la lógica para buscar el producto en la lista de productos
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def handle_search_nit(self):
        """Maneja la búsqueda de cliente por NIT"""
        nit = self.search_bar.text().strip()
        if nit:
            VentasComplementos(self).buscar_cliente_por_nit(nit)
        else:
            QMessageBox.warning(self, "Error", "Ingrese un NIT válido.")

    def buscar_por_descripcion(self):
        """Maneja la búsqueda de productos por descripción"""
        descripcion = self.productos_search_bar.text().strip().lower()
        productos = obtener_stock()
        self.productos_table.setRowCount(0)  # Limpiar la tabla antes de agregar nuevos resultados
        for producto in productos:
            if descripcion in producto['descripcion'].lower():
                row_position = self.productos_table.rowCount()
                self.productos_table.insertRow(row_position)
                self.productos_table.setItem(row_position, 0, QTableWidgetItem(str(producto['id'])))
                self.productos_table.setItem(row_position, 1, QTableWidgetItem(producto['descripcion']))
                self.productos_table.setItem(row_position, 2, QTableWidgetItem(str(producto['precio_venta'])))

    def toggle_widgets_visibility(self, visible):
        """Muestra u oculta los widgets centrales y las barras laterales"""
        self.left_dock.setVisible(visible)
        self.right_dock.setVisible(visible)
        self.search_bar.setVisible(visible)
        self.table.setVisible(visible)
        self.total_label.setVisible(visible)

    def reset_column_colors(self):
        """Restablece los colores de las celdas en la columna de cantidad"""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 3)
            if item:
                item.setForeground(QColor(0, 0, 0))

    def update_total(self):
        """Calcula y actualiza el total general de la venta"""
        total = 0.0
        for row in range(self.table.rowCount()):
            item_subtotal = self.table.item(row, 4)
            if item_subtotal:
                try:
                    subtotal = float(item_subtotal.text())
                    total += subtotal
                except ValueError:
                    pass
        self.total_label.setText(f"Total: {total:.2f}")

    def update_total_facturado(self):
        """Calcula y actualiza el total facturado en la barra de texto correspondiente."""
        update_total_facturado(self)

    def show_nit_dialog(self):
        if not self.iniciar_sesion_action.isEnabled():
            nit_dialog = NitDialog(self)
            if nit_dialog.exec() == QDialog.DialogCode.Accepted:
                nit = nit_dialog.get_nit()
                self.buscar_cliente_por_nit(nit)

    def buscar_cliente_por_nit(self, nit):
        VentasComplementos(self).buscar_cliente_por_nit(nit)

    def show_payment_dialog(self):
        VentasComplementos(self).show_payment_dialog(self.usuario_actual)

    def show_reports(self):
        print("Mostrar reportes")

    def customer_support(self):
        print("Soporte al cliente")

    def view_sales_history(self):
        print("Ver historial de ventas")

    def view_day(self):
        print("Ver día")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())