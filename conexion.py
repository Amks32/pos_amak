import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Superbryan12@',
            database='pos_system'
        )
        if connection.is_connected():
            print("✅ Conexión a la base de datos establecida correctamente")
            return connection
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None  # Devuelve None si falla la conexión

# Otras funciones...

def obtener_usuarios():
    """Obtiene y devuelve todos los usuarios de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor(dictionary=True)
            
            # Ejecuta una consulta para obtener todos los usuarios
            consulta = "SELECT * FROM usuarios"
            cursor.execute(consulta)
            
            # Obtén todos los resultados de la consulta
            usuarios = cursor.fetchall()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return usuarios
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_stock():
    """Obtiene y devuelve todos los productos en stock de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor(dictionary=True)
            
            # Ejecuta una consulta para obtener todos los productos en stock
            consulta = "SELECT * FROM stock"
            cursor.execute(consulta)
            
            # Obtén todos los resultados de la consulta
            productos = cursor.fetchall()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return productos
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_clientes():
    """Obtiene y devuelve todos los clientes de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor(dictionary=True)
            
            # Ejecuta una consulta para obtener todos los clientes
            consulta = "SELECT * FROM clientes"
            cursor.execute(consulta)
            
            # Obtén todos los resultados de la consulta
            clientes = cursor.fetchall()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return clientes
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


def obtener_descuentos():
    """Obtiene y devuelve todos los puntos de los clientes de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor(dictionary=True)
            
            # Ejecuta una consulta para obtener todos los puntos de los clientes
            consulta = "SELECT * FROM descuentos"
            cursor.execute(consulta)
            
            # Obtén todos los resultados de la consulta
            descuentos_activos = cursor.fetchall()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return descuentos_activos
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_puntos_clientes():
    """Obtiene y devuelve todos los puntos de los clientes de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor(dictionary=True)
            
            # Ejecuta una consulta para obtener todos los puntos de los clientes
            consulta = "SELECT * FROM puntos_clientes"
            cursor.execute(consulta)
            
            # Obtén todos los resultados de la consulta
            puntos_clientes = cursor.fetchall()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return puntos_clientes
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def registrar_cliente(cliente):
    """Registra un nuevo cliente en la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            # Crea un cursor para ejecutar consultas
            cursor = conexion.cursor()
            
            # Ejecuta una consulta para registrar un nuevo cliente
            consulta = """
                INSERT INTO clientes (id_cliente, nit_cliente, identificacion, nombre, gmail, telefono, direccion, fecha_registro, fecha_nacimiento, sexo, categoria_cliente, notas)
                VALUES (%(id_cliente)s, %(nit_cliente)s, %(identificacion)s, %(nombre)s, %(gmail)s, %(telefono)s, %(direccion)s, %(fecha_registro)s, %(fecha_nacimiento)s, %(sexo)s, %(categoria_cliente)s, %(notas)s)
            """
            cursor.execute(consulta, cliente)
            
            # Confirma la transacción
            conexion.commit()
            
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            
            return True
        except Error as e:
            print(f"Error al registrar cliente: {e}")
            return False

# Nuevas funciones para las tablas adicionales

def obtener_historial_venta_diaria():
    """Obtiene y devuelve el historial de venta diaria de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM HistorialVentaDiaria"
            cursor.execute(consulta)
            historial = cursor.fetchall()
            cursor.close()
            conexion.close()
            return historial
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_venta_productos_historial():
    """Obtiene y devuelve el historial de venta de productos de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM VentaProductosHistorial"
            cursor.execute(consulta)
            historial = cursor.fetchall()
            cursor.close()
            conexion.close()
            return historial
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_descuentos_y_promociones():
    """Obtiene y devuelve los descuentos y promociones de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM Descuentos_y_Promociones"
            cursor.execute(consulta)
            descuentos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return descuentos
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_historial_de_ventas():
    """Obtiene y devuelve el historial de ventas de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM Historial_de_Ventas"
            cursor.execute(consulta)
            historial = cursor.fetchall()
            cursor.close()
            conexion.close()
            return historial
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_detalles_de_ventas():
    """Obtiene y devuelve los detalles de ventas de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM Detalles_de_Ventas"
            cursor.execute(consulta)
            detalles = cursor.fetchall()
            cursor.close()
            conexion.close()
            return detalles
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_historial_por_cliente():
    """Obtiene y devuelve el historial de ventas por cliente de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM Historial_por_Cliente"
            cursor.execute(consulta)
            historial = cursor.fetchall()
            cursor.close()
            conexion.close()
            return historial
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

def obtener_metodos_de_pago():
    """Obtiene y devuelve los métodos de pago de la base de datos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            consulta = "SELECT * FROM Metodos_de_Pago"
            cursor.execute(consulta)
            metodos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return metodos
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

# Llamar a la función para obtener los usuarios, el stock, los clientes y los puntos de los clientes (solo para pruebas)
if __name__ == "__main__":
    usuarios = obtener_usuarios()
    stock = obtener_stock()
    clientes = obtener_clientes()
    puntos_clientes = obtener_puntos_clientes()
    historial_venta_diaria = obtener_historial_venta_diaria()
    venta_productos_historial = obtener_venta_productos_historial()
    descuentos_y_promociones = obtener_descuentos_y_promociones()
    historial_de_ventas = obtener_historial_de_ventas()
    detalles_de_ventas = obtener_detalles_de_ventas()
    historial_por_cliente = obtener_historial_por_cliente()
    metodos_de_pago = obtener_metodos_de_pago()
    # Aquí puedes hacer algo con los datos obtenidos, por ejemplo, imprimirlos
    print("Usuarios:", usuarios)
    print("Stock:", stock)
    print("Clientes:", clientes)
    print("Puntos Clientes:", puntos_clientes)
    print("Historial Venta Diaria:", historial_venta_diaria)
    print("Venta Productos Historial:", venta_productos_historial)
    print("Descuentos y Promociones:", descuentos_y_promociones)
    print("Historial de Ventas:", historial_de_ventas)
    print("Detalles de Ventas:", detalles_de_ventas)
    print("Historial por Cliente:", historial_por_cliente)
    print("Métodos de Pago:", metodos_de_pago)