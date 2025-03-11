from conexion import obtener_conexion
from mysql.connector import Error
from datetime import datetime

def obtener_nuevo_id_venta():
    """Obtiene el nuevo id_venta sumando uno al último id_venta en la tabla historial_de_ventas."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = "SELECT MAX(id_venta) AS ultimo_id FROM historial_de_ventas"
            cursor.execute(consulta)
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            if resultado and resultado[0]:
                return resultado[0] + 1
            else:
                return 1  # Si no hay registros, el primer id_venta será 1
        except Error as e:
            print(f"Error al obtener el último id_venta: {e}")
            return None

def guardar_historial_venta(id_cliente, usuario, total, efectivo, tarjeta, otros):
    """Guarda una nueva entrada en la tabla historial_de_ventas."""
    nuevo_id_venta = obtener_nuevo_id_venta()
    if nuevo_id_venta is None:
        return False

    fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    venta = {
        'id_venta': nuevo_id_venta,
        'id_cliente': id_cliente,
        'usuario': usuario,
        'fecha_venta': fecha_venta,
        'total': total,
        'efectivo': efectivo,
        'tarjeta': tarjeta,
        'otros': otros
    }

    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """
                INSERT INTO historial_de_ventas (id_venta, id_cliente, usuario, fecha_venta, total, efectivo, tarjeta, otros)
                VALUES (%(id_venta)s, %(id_cliente)s, %(usuario)s, %(fecha_venta)s, %(total)s, %(efectivo)s, %(tarjeta)s, %(otros)s)
            """
            cursor.execute(consulta, venta)
            conexion.commit()
            cursor.close()
            conexion.close()
            return nuevo_id_venta
        except Error as e:
            print(f"Error al guardar el historial de venta: {e}")
            return None

def guardar_detalles_venta(id_venta, tabla_ventas):
    """Guarda los detalles de la venta en la tabla ventas_lista."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            for row in range(tabla_ventas.rowCount()):
                id_producto = int(tabla_ventas.item(row, 0).text())
                descrpcion = tabla_ventas.item(row, 1).text()
                cantidad = int(tabla_ventas.item(row, 3).text())
                precio_unitario = float(tabla_ventas.item(row, 2).text())
                precio_descuento = float(tabla_ventas.item(row, 5).text()) if tabla_ventas.item(row, 5) else 0.0
                precio_promocion = float(tabla_ventas.item(row, 6).text()) if tabla_ventas.item(row, 6) else 0.0
                precio_mayorista = float(tabla_ventas.item(row, 7).text()) if tabla_ventas.item(row, 7) else 0.0

                detalle_venta = {
                    'id_venta': id_venta,
                    'id_producto': id_producto,
                    'descrpcion': descrpcion,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'precio_descuento': precio_descuento,
                    'precio_promocion': precio_promocion,
                    'precio_mayorista': precio_mayorista
                }

                consulta = """
                    INSERT INTO ventas_lista (id_venta, id_producto, descrpcion, cantidad, precio_unitario, precio_descuento, precio_promocion, precio_mayorista)
                    VALUES (%(id_venta)s, %(id_producto)s, %(descrpcion)s, %(cantidad)s, %(precio_unitario)s, %(precio_descuento)s, %(precio_promocion)s, %(precio_mayorista)s)
                """
                cursor.execute(consulta, detalle_venta)

            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print(f"Error al guardar los detalles de la venta: {e}")
            return False