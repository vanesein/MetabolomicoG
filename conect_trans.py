import os;
import psycopg2


#obtiene la conexion de base de datos, en este caso es postgres y se usa el driver psycog2 para la comunicacion
def get_base_connection(database , usuario , contrasena):
    conn = psycopg2.connect(database= database, user= usuario, host="127.0.0.1", port="5432")
    return conn

#obtiene un cursor de la base de datos
def get_cursor (connection):
    cur = connection.cursor()
    return cur

#ejecuta select y devuelve las filas
def execute_select (cursor , sql):
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

#ejecuta una transaccion en la base de datos
def execute_transaction (connection , cursor , sql):
    cursor.execute(sql)
    connection.commit()

#cierra conexion
def close_connection(connection):
    connection.close()

#guarda la linea procesada en una tabla temporal en la base de datos
def guardar_linea(connection , cursor , nombre , tipo , indice , linea):
    sentencia = "insert into archivos (inidice_linea , linea) values ( " + str(indice) + " , '" + linea + "')"
    execute_transaction(connection , cursor , sentencia)

#funcion auxiliar (no usada) guarda cada atributo de un objeto pfile
def guardar_atributos(connection , cursor , arg , line , tipo):
    sentencia = "insert into archivos(nombre_archivo , tipo_archivo , indice_linea , linea , retention_time , first_scan , max_scan , last_scan , pk_ty , peak_height , concentracion , corr_max_porc , por_tot) values ('" + arg.file_name + "' , '" + tipo + "' , " + arg.index + " , '" + line + "' , " + arg.retention_time + " , " + arg.first_scan + " , " + arg.max_scan + " , " + arg.last_scan + " , '" + arg.pk + " " + arg.ty + "' , '" + arg.peak_height + "' , '" + arg.corr_area + "' , '" + arg.corr_max + "' , '" + arg.por_tot + "' )"
    execute_transaction(connection , cursor , sentencia)


#funcion auxiliar (no usada) actualiza la linea
def actualizar_linea(connection , cursor , nombre_archivo , indice , linea):
    sentencia = "update archivos set linea = '" + linea + "' where nombre_archivo = '" + nombre_archivo + "' and inidice_linea = '" + str(indice) + "'"
    execute_transaction(connection , cursor , sentencia)

#funcion auxiliar (no usada) obtengo los nombres de archivos
def obtener_archivos (connection , cursor):
    sentencia = "select distinct (nombre_archivo) from archivos"
    filas = execute_select(cursor , sentencia)
    return filas

#obtengo el numero de filas pertenecientes a cada archivo
def obtener_numero_lineas_archivo(connection , cursor , nombre_archivo):
    sentencia = "select count(*) from archivos where nombre_archivo = '" + nombre_archivo + "' "
    numero = execute_select_count(cursor , sentencia)
    return int(numero[0])

#obtengo una fila de acuerdo a un indice
def obtener_fila(connection , cursor , indice):
    sentencia = "select linea from archivos where inidice_linea = '" + str(indice) + "'"
    linea = execute_select(cursor , sentencia)
    return ((linea[0])[0]) # el string del primero de la tupla de la primera posicion de la lista

#obtengo una cantidad (select count)
def execute_select_count(cursor , sql):
    cursor.execute(sql)
    cantidad = cursor.fetchone()
    return cantidad

#borra la tabla temporal para la siguiente ejecucion
def borrar_tabla_temporal(connection , cursor):
    sentencia = "delete from archivos"
    execute_transaction(connection , cursor , sentencia)

#def create_tb_results(connection , cursor, num_columns):
#
#	sentencia = "CREATE TABLE Cars(oid INTEGER PRIMARY KEY, intervalo_time DOUBLE, intensidad_aceptacion INT, min_interval_confianza INT, max_interval_confianza INT, "
#
#	for x in xrange(1,num_columns):
#		sentencia .= sentencia
#
		#
#    execute_transaction(connection , cursor , sentencia)


#guarda la linea procesada en una tabla temporal en la base de datos
def guardar_result(connection , cursor , oid, nombre_destino, intervalo_time, intensidad_aceptacion, min_interval_confianza, max_interval_confianza, line_result):
    sentencia = "insert into resultados (oid, intervalo_time, intensidad_aceptacion, min_interval_confianza,max_interval_confianza, line_result, archivo) values ("+str(oid)+", "+str(intervalo_time)+",  "+str(intensidad_aceptacion)+" , "+str(min_interval_confianza)+" , "+str(max_interval_confianza)+" ,'" + line_result + "' ,'" + nombre_destino + "')"
    execute_transaction(connection , cursor , sentencia)


def select_max_oid_result(connection , cursor ):
	sentencia = "select CASE WHEN max(oid)+1 is null then 1 else max(oid)+1 end as total from resultados"
	rows = execute_select(cursor , sentencia)	
	#total = rows[0]["total"]
	total = ((rows[0])[0])
	return total

def select_max_oid_result_process(connection, cursor):
	sentencia = "select CASE WHEN max(oid)+1 is null then 1 else max(oid)+1 end as total from procesos"
	rows = execute_select(cursor , sentencia)	
	#total = rows[0]["total"]
	total = ((rows[0])[0])
	return total

def guardar_info_proces(connection, cursor, last_oid_proceso, tiempo_ejecucion_alineamiento, tiempo_ejecucion_proceso, intervalo_time, intensidad_aceptacion, min_interval_confianza, max_interval_confianza, file_destino, num_alineaciones):
    sentencia = "insert into procesos (oid, tiempo_ejecucion_alineamiento, tiempo_ejecucion_proceso, intervalo_time, intensidad_aceptacion, min_interval_confianza, max_interval_confianza, archivo, num_alineaciones) values ("+str(last_oid_proceso)+", "+str(tiempo_ejecucion_alineamiento)+",  "+str(tiempo_ejecucion_proceso)+" , "+str(intervalo_time)+", "+ str(intensidad_aceptacion)+", "+str(min_interval_confianza)+" , "+str(max_interval_confianza)+", '" + file_destino + "', "+ str(num_alineaciones)+")"
    execute_transaction(connection , cursor , sentencia)
