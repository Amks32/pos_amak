from conexion import obtener_stock, obtener_descuentos
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor
from decimal import Decimal

def obtener_valor_busqueda(main_window):
    """Obtiene el valor de la barra de búsqueda y lo convierte en un número entero."""
    # Cambiar el color de todas las celdas al principio de la función
    for row in range(main_window.table.rowCount()):
        for col in range(main_window.table.columnCount()):
            item = main_window.table.item(row, col)
            if item:
                item.setForeground(QColor(255, 255, 255))
                item.setBackground(QColor(0, 0, 0))

    input_text = main_window.search_bar.text().strip()
    if not input_text:
        raise ValueError("Ingrese un ID de producto válido.")
    
    try:
        if '*' in input_text:
            cantidad, id_busqueda = input_text.split('*')
            cantidad = Decimal(cantidad)
            id_busqueda = int(id_busqueda)
        else:
            cantidad = Decimal(1.0)
            id_busqueda = int(input_text)
    except ValueError:
        raise ValueError("El ID del producto debe ser un número entero.")
    
    # Llamar a obtener_stock y comparar el valor de id
    productos = obtener_stock()
    descuentos = obtener_descuentos()
    for producto in productos:
        if producto['id'] == id_busqueda:
            print("Valor encontrado")
            # Calcular el subtotal
            precio_venta = Decimal(producto['precio_venta'])
            subtotal = precio_venta * cantidad
            
            # Verificar si el ID ya existe en la tabla
            for row in range(main_window.table.rowCount()):
                item = main_window.table.item(row, 0)
                if item and int(item.text()) == id_busqueda:
                    # Actualizar la cantidad y el subtotal
                    current_quantity = Decimal(main_window.table.item(row, 3).text())
                    new_quantity = current_quantity + cantidad
                    new_subtotal = precio_venta * new_quantity
                    main_window.table.setItem(row, 3, QTableWidgetItem(str(new_quantity)))
                    main_window.table.setItem(row, 4, QTableWidgetItem(f"{new_subtotal:.2f}"))
                    
                    # Evaluar el descuento
                    descuento = 0.0
                    for descuento_item in descuentos:
                        if descuento_item['id'] == id_busqueda:
                            if new_quantity >= Decimal(descuento_item['cantidad']):
                                descuento = Decimal(descuento_item['precio'])
                                main_window.table.setItem(row, 5, QTableWidgetItem(f"{descuento:.2f}"))
                            else:
                                row_position = main_window.ofertas_table.rowCount()
                                main_window.ofertas_table.insertRow(row_position)
                                main_window.ofertas_table.setItem(row_position, 0, QTableWidgetItem(descuento_item['tipo_de_promocion']))
                                main_window.ofertas_table.setItem(row_position, 1, QTableWidgetItem(descuento_item['descripcion']))
                                main_window.ofertas_table.setItem(row_position, 2, QTableWidgetItem(f"{descuento_item['precio']:.2f}"))
                    
                    # Evaluar la promoción
                    if producto['columna_extra_1'] is not None and new_quantity >= Decimal(producto['columna_extra_1']):
                        descuento_promocion = (precio_venta - Decimal(producto['precio_oferta_2'])) * new_quantity
                        main_window.table.setItem(row, 6, QTableWidgetItem(f"{descuento_promocion:.2f}"))
                    else:
                        main_window.table.setItem(row, 6, QTableWidgetItem("0.00"))
                    
                    # Evaluar el mayorista
                    if producto['columna_extra_2'] is not None and new_quantity >= Decimal(producto['columna_extra_2']):
                        descuento_mayorista = (precio_venta - Decimal(producto['precio_oferta_3'])) * new_quantity
                        main_window.table.setItem(row, 7, QTableWidgetItem(f"{descuento_mayorista:.2f}"))
                    else:
                        main_window.table.setItem(row, 7, QTableWidgetItem("0.00"))
                    
                    # Marcar la celda actualizada
                    main_window.table.item(row, 3).setForeground(QColor(255, 255, 255))
                    main_window.table.item(row, 4).setForeground(QColor(255, 255, 255))
                    main_window.table.item(row, 5).setForeground(QColor(255, 255, 255))
                    main_window.table.item(row, 6).setForeground(QColor(255, 255, 255))
                    main_window.table.item(row, 7).setForeground(QColor(255, 255, 255))
                    
                    main_window.update_total()
                    main_window.search_bar.clear()
                    main_window.update_total_facturado()
                    return id_busqueda
            
            # Agregar una nueva fila a la tabla
            row_position = main_window.table.rowCount()
            main_window.table.insertRow(row_position)
            main_window.table.setItem(row_position, 0, QTableWidgetItem(str(producto['id'])))
            main_window.table.setItem(row_position, 1, QTableWidgetItem(producto['descripcion']))
            main_window.table.setItem(row_position, 2, QTableWidgetItem(str(precio_venta)))
            main_window.table.setItem(row_position, 3, QTableWidgetItem(str(cantidad)))
            main_window.table.setItem(row_position, 4, QTableWidgetItem(f"{subtotal:.2f}"))
            
            # Evaluar el descuento
            descuento = 0.0
            for descuento_item in descuentos:
                if descuento_item['id'] == id_busqueda:
                    if cantidad >= Decimal(descuento_item['cantidad']):
                        descuento = Decimal(descuento_item['precio'])
                        main_window.table.setItem(row_position, 5, QTableWidgetItem(f"{descuento:.2f}"))
                    else:
                        row_position_ofertas = main_window.ofertas_table.rowCount()
                        main_window.ofertas_table.insertRow(row_position_ofertas)
                        main_window.ofertas_table.setItem(row_position_ofertas, 0, QTableWidgetItem(descuento_item['tipo_de_promocion']))
                        main_window.ofertas_table.setItem(row_position_ofertas, 1, QTableWidgetItem(descuento_item['descripcion']))
                        main_window.ofertas_table.setItem(row_position_ofertas, 2, QTableWidgetItem(f"{descuento_item['precio']:.2f}"))
            
            # Evaluar la promoción
            if producto['columna_extra_1'] is not None and cantidad >= Decimal(producto['columna_extra_1']):
                descuento_promocion = (precio_venta - Decimal(producto['precio_oferta_2'])) * cantidad
                main_window.table.setItem(row_position, 6, QTableWidgetItem(f"{descuento_promocion:.2f}"))
            else:
                main_window.table.setItem(row_position, 6, QTableWidgetItem("0.00"))
            
            # Evaluar el mayorista
            if producto['columna_extra_2'] is not None and cantidad >= Decimal(producto['columna_extra_2']):
                descuento_mayorista = (precio_venta - Decimal(producto['precio_oferta_3'])) * cantidad
                main_window.table.setItem(row_position, 7, QTableWidgetItem(f"{descuento_mayorista:.2f}"))
            else:
                main_window.table.setItem(row_position, 7, QTableWidgetItem("0.00"))
            
            # Marcar las celdas de la nueva fila
            for col in range(8):
                item = main_window.table.item(row_position, col)
                if item is None or item.text() == "":
                    main_window.table.setItem(row_position, col, QTableWidgetItem("0"))
                else:
                    item.setForeground(QColor(255, 255, 255))
            
            main_window.update_total()
            main_window.search_bar.clear()
            main_window.update_total_facturado()
            return id_busqueda
    else:
        print("Valor no encontrado")
        raise ValueError("Producto no encontrado")

def update_total_facturado(main_window):
    """Calcula y actualiza el total facturado en la barra de texto correspondiente."""
    total_facturado = 0.0
    total_promocion = 0.0
    total_mayorista = 0.0
    facturado_en_promocion = 0.0
    for row in range(main_window.table.rowCount()):
        item_subtotal = main_window.table.item(row, 4)
        item_descuento = main_window.table.item(row, 5)
        item_promocion = main_window.table.item(row, 6)
        item_mayorista = main_window.table.item(row, 7)
        if item_descuento and float(item_descuento.text()) > 0:
            try:
                descuento = float(item_descuento.text())
                cantidad = float(main_window.table.item(row, 3).text())
                facturado_en_promocion += descuento * cantidad
            except ValueError:
                pass
        elif item_subtotal and (item_descuento is None or float(item_descuento.text()) == 0):
            try:
                subtotal = float(item_subtotal.text())
                total_facturado += subtotal
            except ValueError:
                pass
        if item_promocion and (item_mayorista is None or float(item_mayorista.text()) == 0):
            try:
                promocion = float(item_promocion.text())
                total_promocion += promocion
            except ValueError:
                pass
        if item_mayorista:
            try:
                mayorista = float(item_mayorista.text())
                total_mayorista += mayorista
            except ValueError:
                pass
    main_window.venta_fields["Total Facturado"].setText(f"{total_facturado:.2f}")
    main_window.venta_fields["Descuento Promoción"].setText(f"{total_promocion:.2f}")
    main_window.venta_fields["Descuento Mayorista"].setText(f"{total_mayorista:.2f}")
    main_window.venta_fields["Facturado en Promoción"].setText(f"{facturado_en_promocion:.2f}")
    
    # Calcular el total final
    total_final = total_facturado + facturado_en_promocion - total_promocion - total_mayorista
    main_window.venta_fields["TOTAL"].setText(f"{total_final:.2f}")