#!/usr/bin/python
#! -*- coding: utf-8 -*-

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


#'''--------------------------------------------------------------
#Autor: Isaac Torres Bermeo, vanessa Heredia
#Afiliación: CVR, CIBE, CTI
#Versión: 5
#'''-------------------------------------------------------------


import os;
import psycopg2
#from tkinter import messagebox
import xlwt

import linecache
import math
import time

from conect_trans import *
from settings import logging

#clase que representa a un compuesto (fila del archivo)
class pfile(object):

    index = 0
    retention_time = 0
    max_scan = 0
    fragments = ""
    file_name = ""
    bandera_cambio = 0
    corr_area = ''
    retention_time_promedio = 0
    index_file = 0
    pareja = False
    checked = False
    savert = False

    #a partir de aquí no importa, es sólo para llenar el archivo
    peak = ''
    first_scan = ''
    last_scan = ''
    pk = ''
    ty = ''
    peak_height = ''
    corr_max = ''
    por_tot = ''
    

#class
class cfile(object):
    pos = 0
    rt = 0
    rtp = 0
    corr_area = ',0000000000'
    checked = False

#class
class nline(object):
    pos = 0
    value = 0

#quita la extension de cada nombre de archivo de una lista
def arregla_nombres(name):
    f = []
    for fln in name:
        f.append(os.path.basename(fln))
    return f

#quita la extension del nombre de archivo de una lista de objetos tipo pfile
def arregla_nombres_objeto (l_obj):
    for obj in l_obj:
        obj.file_name = obj.file_name.split('.')[0]

#verifica si un string es un númerohttp://www.samsung.com/ae/smarthub/html/screen.html
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#valida si el campo ty de la linea leida es nulo
def valida_decima_posicion(str):
    try:
        str.split()[10]
        return True
    except :
        return False


#get minimum retention time from first lines of all documents
def min_retention_time(path_porc, porcentaje_names):
    rt = []
    
    for p in porcentaje_names:
        line = linecache.getline(path_porc + '/' + p, 23)
        num = line.split()[1]
        if (is_number(num)== True) :
            rt.append(float(num))
    min_num = min(rt)
    return math.trunc(min_num)         

# gets the sum of each fragment, define 90% of similarity and compares fragments according the 90%
def compare_fragments(linea_uno , linea_dos, min_range_accepted, min_porcent_range, max_porcent_range):
    temp = linea_uno.split(",") #extraigo los elementos separados por comas y los guardo en una lista
    temp2 = linea_dos.split(",")

    (total_linea1 , total_linea2, porcent, linea1, linea2) = suma_linea(temp , temp2, min_range_accepted) #sumo los elementos que separé por comas

    bandera  = compare_mz(linea1, linea2, porcent, total_linea1, total_linea2, min_porcent_range, max_porcent_range)

    if len(temp) == 1 : #para evitar comparaciones entre elementos nulos, ya que afectan todo el proceso
        bandera = False

    return bandera ###si los porcentajes estan dentro dl rango 

# sumo los elementos de cada linea y retorno ambas sumatorias
# no include the elements lof fragments are ess 50000 (noise intensity)
# defines the 90% of numbers that must be similar; 90% final is defined by the fragment having the fewest numbers
# no include the elements lof fragments are ess 50000 (noise intensity)
def suma_linea (linea_uno , linea_dos, min_range_accepted): 
    total_temp = 0
    total_temp2 = 0

    count_elem1 = 0
    count_elem2 = 0
    new_line1 = []
    new_line2 = []
    porcent = 0

    for i in range(0 , len(linea_uno) -1 ):
        esp = (linea_uno[i]).strip()
        if (is_number(esp) == True):
            if ((float(esp) > 0) and (float(esp) >= min_range_accepted)):
                count_elem1+=1
            line = nline()
            line.value = float(esp)
            line.pos = i
            new_line1.append(line)

    for i in range(0 , len(linea_dos) -1 ):
        esp2 = (linea_dos[i]).strip()
        if (is_number(esp2) == True):
            if ((float(esp2) > 0) and (float(esp2) >= min_range_accepted)):
                count_elem2+=1
            line = nline()
            line.value = float(esp2)
            line.pos = i
            new_line2.append(line)

    print("count_elem1 "+str(count_elem1) + " --- " + "count_elem2 "+str(count_elem2))

    new_line1.sort(key = lambda x: x.value, reverse=True)
    new_line2.sort(key = lambda x: x.value, reverse=True)
    line1 = []
    line2 = []

    if(count_elem1>=count_elem2):
        porcent = round(count_elem2 * 0.9)

        for i in range(0 , count_elem1 ):
            total_temp = total_temp +  new_line1[i].value
            line = nline()
            line.value = new_line1[i].value
            line.pos = new_line1[i].pos
            line1.append(line)

        for i in range(0 , count_elem1 ):
            total_temp2 = total_temp2 +  new_line2[i].value
            line = nline()
            line.value = new_line2[i].value
            line.pos = new_line2[i].pos
            line2.append(line)

    else:
        porcent = round(count_elem1 * 0.9)
        for i in range(0 , count_elem2 ):
            total_temp = total_temp +  new_line1[i].value
            line = nline()
            line.value = new_line1[i].value
            line.pos = new_line1[i].pos
            line1.append(line)

        for i in range(0 , count_elem2 ):
            total_temp2 = total_temp2 +  new_line2[i].value
            line = nline()
            line.value = new_line2[i].value
            line.pos = new_line2[i].pos
            line2.append(line)

    print("total_linea1 "+str(total_temp))
    print("total_linea2 "+str(total_temp2))

    total_temp = 1 if (total_temp==0) else total_temp
    total_temp2 = 1 if (total_temp2==0) else total_temp2

    return (total_temp , total_temp2, porcent, line1, line2)


# compares the fragments, for that the method compare relative intensity of each element of the fragment in the same position
# no include the elements lof fragments are ess 50000 (noise intensity) and cero matches
# returns true if the number of matches are greater or equal to 90%
def compare_mz(mz1 , mz2, porcent_90, total_linea1, total_linea2, min_porcent_range, max_porcent_range):
    countn = 0

    for i in range(0 , len(mz1)):
        esp = mz1[i].value
        for j in range(0 , len(mz2)):
            if (mz1[i].pos==mz2[j].pos):
                esp2 = mz2[j].value
                s = "pos: "+str(mz2[j].pos) +" - esp: " + str(esp) + "--- esp2 "+str(esp2)
                print(s)
                if (compare_mz_porcent((float(esp) * 100)/total_linea1, (float(esp2)*100)/total_linea2, min_porcent_range, max_porcent_range) == True): #comparo los elementos con la regla del 10%
                    print("porc1: "+ str((float(esp) * 100)/total_linea1) + "--- porc2: "+ str((float(esp2) * 100)/total_linea2))
                    countn += 1 #si es falso la bandera se hace 0 y sale del lazo porque no tiene sentido comparar el resto

    print("despues compare_mz con coincidencias: "+str(countn) + " -- porcent_90: " + str(porcent_90))

    if ((int(porcent_90) > 0)  and (int(countn) > 0 )):        
        if (int(countn) >= int(porcent_90)):
            print("numeros q coincideieron: "+ str(countn))
            return True
        else:
            return False
    else:
        return False


# compares the relative intensity, depending on which is the highest percentage is calculed its 15%
# to extend the range of similarity
def compare_mz_porcent (porcent1 , porcent2, min_porcent_range, max_porcent_range):
    if(porcent1>=porcent2): 
        limit1 = round((porcent1 - (min_porcent_range * porcent1)),2)
        limit2 = round((porcent2 + (max_porcent_range * porcent2)),2)

        if (porcent2>=limit1 and porcent1>=limit2) or (limit1>=porcent2 and limit2>=porcent1) or (limit2>=porcent1 and limit2>=limit1) or (limit1>=porcent2 and limit2>=limit1):
            return True
        else:
            return False
    elif(porcent2>=porcent1):
        limit2 = round((porcent2 - (min_porcent_range * porcent2)),2)
        limit1 = round((porcent1 + (max_porcent_range * porcent1)),2)

        if (porcent1>=limit2 and porcent2>=limit1) or (limit2>=porcent1 and limit1>=porcent2) or (limit1>=porcent2 and limit1>=limit2) or (limit2>=porcent1 and limit1>=limit2):
            return True
        else:
            return False
    else:
        return False


# creo la cabecera del archivo
def crear_cabecera(num_archivos ):
    linea = "Retention time"

    for i in range(1 , num_archivos + 1): # esta parte es dinámica, se la llena de acuerdo al número de días
        linea = linea + ",D" + str(i)

    return linea

# armo la primera parte de cada linea del archivo resultante, la cual es fija
def armar_linea_base (L_procesar , indice) :
    temporal = L_procesar[indice - 1]
    linea_base = str(round(temporal.retention_time_promedio,3))
    return (linea_base , temporal)


#función principal, recibe la ruta del directorio de archivos de compuestos, ruta de archivos de matrices, rango de tiempo de medición, nombre del archivo de destino
def MainProcess(connection, cursor, path_porc, path_mat, porcentaje_names, matriz_names, path_dest , intervalo_time, file_destino, min_range_accepted, min_porcent_range, max_porcent_range):

    time1 = time.time()
    
    try:
        
        #get minimum retention time from first lines of all documents
        min_ret_time = min_retention_time(path_porc, porcentaje_names)
        
        #voy a recoger los elementos que caigan en este rango, comienza de 0
        contador_minutos = min_ret_time
        #print("contador_minutos "+str(contador_minutos))
        #lista de elementos a procesar en cada rango de tiempo
        L_procesar = []
        i = 1
        contador_archivos = 0
        num_alineaciones = 0
        
        #de 0 a 30 minutos
        while (contador_minutos <= 30):
            print("intervalo_time: min: " + str(contador_minutos - intervalo_time) + " -- max: "+str(contador_minutos))
            L_procesar = []
            #bandera para contar los archivos
            contador_archivos = 0

            #recorro cada archivo pasando por las lineas que cumplen con RT dentro de los rangos stablecidos
            #considera q solo toma una linea x archivo o evita que se seleccionen 2 o mas elementos en cada retention_time
            #aquellos q cumplen se guardan en L_procesar y si hay lineas q no cumplen se guarda un pfile con valores nulos
            for p in porcentaje_names:
                contador_archivos = contador_archivos + 1
                #bandera para determinar que sólo se escoja un elemento por archivo
                contador_lineas = 0
                for index, line in enumerate(open(path_porc + '/' + p)):  # validar desde donde comienza la data (23)
                    #si lo pongo en un and no funciona
                    if line != '\n':
                        #si lo pongo en un and no funciona
                        if line != ' \n':
                            #si el indice es la linea 23 y el retention_time es un número
                            if (index >= 22) and (is_number(line.split()[1]) == True):
                                #si el retention_time esta en el rango indicado
                                if (float(line.split()[1]) < contador_minutos) and (float(line.split()[1]) >= (contador_minutos - intervalo_time)) :
                                    #si es el primer elemento del archivo q estoy cogiendo (evita que se seleccionen 2 o mas elementos en cada retention_time
                                    arg = pfile() #creo y doty memoria a un objeto pfile
                                    arg.file_name = p #p[:10] #nombre dl archivo
                                    arg.max_scan = float(line.split()[3]) #scan máximo
                                    arg.retention_time = float(line.split()[1]) #retention_time
                                    arg.retention_time_promedio = float(line.split()[1])
                                    #introducir aquí el resto de valores
                                    arg.peak = line.split()[0] #
                                    arg.first_scan = line.split()[2]
                                    arg.last_scan = line.split()[4]
                                    arg.pk = line.split()[5]
                                    arg.index_file = contador_archivos
                                    if (valida_decima_posicion(line) == True): # si existe o no el nuemro que acompana al campo ty en essa linea
                                        arg.ty = line.split()[6]
                                        arg.peak_height = line.split()[7]
                                        arg.corr_area = line.split()[8] #concentración
                                        arg.corr_max = line.split()[9]
                                        arg.por_tot = line.split()[10]
                                    else:
                                        arg.ty = ''
                                        arg.peak_height = line.split()[6]
                                        arg.corr_area = line.split()[7] #concentración
                                        arg.corr_max = line.split()[8]
                                        arg.por_tot = line.split()[9]


                                    L_procesar.append(arg) #lista que procesa archivos   

                L_procesar.sort(key = lambda x: x.retention_time)


            #sobre el Lprocesar que tiene los obj pfile con aquellos que cumplian el rango de cada firle
            #se procede a llenar el elemento fragments de cada objeto pfile con su correspondiente nombre de archivo de matriz
            #y su indice de max_scan 
            matriz_names = arregla_nombres(matriz_names) #remuevo las extensiones de los archivos
            arregla_nombres_objeto(L_procesar) #remuevo las extensiones de los archivos
            #para cada registro de la lista a procesar, encuentro su línea de fragmentos en el archivo de matriz
            for p in matriz_names:
                # for de cada muestra
                for q in L_procesar:
                    if p == q.file_name:
                        for index , line in enumerate(open(path_mat + '/' + p)):
                            if (index == (q.max_scan + 4)) and (q.max_scan > 0):
                                q.fragments = line.partition(',')[2] #partition da una tupla ej "AB-CD-EF".partition('-') = ('AB', '-', 'CD-EF')


            
            #print("len de L_procesar: "+ str(len(L_procesar)))
            #for x in range(0,len(L_procesar)):
            #    print ("pos d L_procesar q existen: " + str(L_procesar[x].index_file) + "bandera_cambio: " + str(L_procesar[x].bandera_cambio))




            #se compara los fragments de un file con el resto de files, si es el mismo file no se copmpara
            # cada par gragmentos se considera la suma total del fragmento y se verificar si esta dentro del 
            # 10% en caso de q sean iguales tonces el indice de la bandera_contador (es posicion o numero d file) es igual para todos aquellos q coincidan 
            bandera_contador = 0
            for p in L_procesar:
                #bandera_continuar = 0 #indica si el proceso de comparacion continua
                bandera_contador += 1 

                if (p.bandera_cambio == 0 and p.pareja==False): #el elemento no se ha alineado con otro todavía

                    p.bandera_cambio = bandera_contador #le pongo el índice correspondiente
                    #bandera_continuar = 1 # permitirá la búsqueda de elementos con los cuales posiblemente se alinee
                #if bandera_continuar == 1 :
                    for q in L_procesar:
                        #si no se trata de un mismo elemento & si no ha sido alineado antes
                        #if ( p.file_name != q.file_name) & 
                        if(q.bandera_cambio == 0):
                            #si la comparacion entre fragmentos es buena
                            #if (comparar_fragmentos(p.fragments,q.fragments) == 1):
                            #print("*********")
                            #print(p.file_name)
                            #print("RT: "+ str(p.retention_time)+" MaxScan: " + str(p.max_scan))
                            #print(q.file_name)
                            #print("RT: "+ str(q.retention_time)+" MaxScan: " + str(q.max_scan))
                            #print("*********")
                            if (compare_fragments(p.fragments, q.fragments, min_range_accepted, min_porcent_range, max_porcent_range) == True):
                                #print("bandera_contador" + str(bandera_contador))
                                p.bandera_cambio = bandera_contador    
                                q.bandera_cambio = bandera_contador
                                q.pareja = True
                                p.pareja = True
                            #poner bandera a ambos elementos para ver que han sido cambiados

            print("len de L_procesar: "+ str(len(L_procesar)))
            for x in range(0,len(L_procesar)):
                print ("L_procesar q existen desoes d comprar fragments: " + str(L_procesar[x].retention_time)+ " pos: "+str(L_procesar[x].index_file) + " bandera_cambio: " + str(L_procesar[x].bandera_cambio) + "pareja: "+str(L_procesar[x].pareja))


            # funcion para arreglar el promedio de los tiempos de retención
            # se suma los RT de todos los q coinciden las banderas_cambio que fueron iguales a la pos de files q coincidieron
            # en el paso anterior con su bandera_contador
            promedio = 0
            cont_elementos = 0
            for p in range(0,len(L_procesar)):
                flag = 0
                #print ("viendo p : " + str(L_procesar[p].retention_time)+ " bandera_cambio: " + str(L_procesar[p].bandera_cambio) + "pareja: "+str(L_procesar[p].pareja))
                if (p<len(L_procesar)):
                    for q in range(p+1,len(L_procesar)):
                        #print ("viendo q : " + str(L_procesar[q].retention_time)+ " bandera_cambio: " + str(L_procesar[q].bandera_cambio) + "pareja: "+str(L_procesar[q].pareja))
                        if(L_procesar[p].bandera_cambio == L_procesar[q].bandera_cambio and L_procesar[q].pareja==True):
                            #print("si entro a calc prom")
                            promedio = promedio + L_procesar[q].retention_time
                            cont_elementos += 1
                            flag = 1
                            
                    if (flag == 1):
                        promedio = promedio + L_procesar[p].retention_time
                        cont_elementos += 1

                        for q in range(p+1,len(L_procesar)):
                            if(L_procesar[p].bandera_cambio == L_procesar[q].bandera_cambio and L_procesar[q].pareja==True):
                                L_procesar[p].retention_time_promedio = promedio/cont_elementos
                    
                        promedio = 0
                        cont_elementos = 0


            
            last_oid = select_max_oid_result(connection, cursor)
            
            #se escoge aquellos Lprocesar que deben ser guardados en el archivo de salida
            for p in L_procesar:
                C_procesar = []
                #print ("escogiendo pares p con : " + str(p.retention_time)+ " pos: "+str(p.index_file) + " bandera_cambio: " + str(p.bandera_cambio) + " pareja: "+str(p.pareja) + " savert"+str(p.savert) + " checked"+str(p.checked))
                if(p.checked==False and p.savert ==False):
                    p.checked = True
                    p.savert = True
                    cpfile = cfile()
                    cpfile.pos = p.index_file
                    cpfile.rt = round(p.retention_time,3)
                    cpfile.corr_area = p.corr_area
                    cpfile.rtp = p.retention_time_promedio
                    cpfile.checked = False
                    C_procesar.append(cpfile)
                    
                    for q in L_procesar:
                        if (q.checked==False and q.savert == False):
                            #print ("escogiendo pares q con : " + str(q.retention_time)+ " pos: "+str(q.index_file) + " bandera_cambio: " + str(q.bandera_cambio) + " pareja: "+str(q.pareja) + " savert"+str(q.savert) + " checked"+str(q.checked))
                            if (p.bandera_cambio == q.bandera_cambio):
                                if (p.index_file != q.index_file):
                                    cpfile = cfile()
                                    cpfile.pos = q.index_file
                                    cpfile.rt = round(q.retention_time,3)
                                    cpfile.corr_area = q.corr_area
                                    cpfile.rtp = q.retention_time_promedio
                                    cpfile.checked = False
                                    C_procesar.append(cpfile)
                                    q.checked = True
                                    p.savert = True
                                    
                                else:
                                    q.checked = True
                                   

                    #print("tam de C_procesar: "+ str(len(C_procesar)))


                    if(len(C_procesar)>0):
                        C_procesar.sort(key = lambda x: x.pos)
                        
                        #for x in range(0,len(C_procesar)):
                        #    print ("pos d C_procesar q existen d lproc *** : " + str(C_procesar[x].pos) + "- rt: "+str(C_procesar[x].rt)+ "- rt prom: "+str(C_procesar[x].rt)+ "checked: "+ str(C_procesar[x].checked))

                        aux = 1
                        a= 0
                        while(aux<len(porcentaje_names)+1):
                            #print("pos comparar x : "+str(aux) +"  y x C_procesar: "+ str(C_procesar[a].pos))

                            if(C_procesar[a].pos == aux):
                                
                                if(len(C_procesar) == aux):
                                    aux+=1
                                else:
                                    a+=1
                                    aux+=1
                            else:
                                cpfile = cfile()
                                cpfile.pos = aux
                                cfile.rt = -1
                                C_procesar.append(cpfile)
                                aux+=1


                        
                        C_procesar.sort(key = lambda x: x.pos)

                            
                        for x in range(0,len(C_procesar)):
                            print ("pos d C_procesar q existen d lproc --- : " + str(C_procesar[x].pos) + "- rt: "+str(C_procesar[x].rt)+ "- rt prom: "+str(C_procesar[x].rtp))        


                        #for x in range(0,len(C_procesar)):
                        #    print ("pos d C_procesar final: " + str(C_procesar[x].pos))
                        base_line =  str(round(p.retention_time_promedio,3))
                        
                        count_no_aling_in_line = 0

                        for x in range(0,len(porcentaje_names)):
                            if (C_procesar[x].rt == -1):
                                base_line = base_line + "," + str(0)
                                count_no_aling_in_line +=1
                            else:
                                base_line = base_line + "," + str(round(C_procesar[x].rt,3)) + "|" + C_procesar[x].corr_area

                        num_alineaciones += 1 if (count_no_aling_in_line < len(porcentaje_names)-1) else 0
                        
                        guardar_linea(connection, cursor, 'NO USO', 'POR', i, base_line)

                        guardar_result(connection, cursor, last_oid, file_destino, intervalo_time, min_range_accepted, min_porcent_range, max_porcent_range ,base_line)
                        last_oid += 1
                        i += 1


            # continuo con el siguiente rango
            contador_minutos = contador_minutos + intervalo_time

        time2 = time.time()
        tiempo_ejecucion_alineamiento = time2 - time1

        # Una vez terminado con los rangos, genero los archivos a partir de información de la BD
        archivo = open(path_dest + '/' + file_destino + '.csv', 'w')
        #cabecera del archivo
        linea_cabecera = crear_cabecera(len(porcentaje_names))
        #escribo la cabecera en el archivo
        archivo.write(linea_cabecera + "\n")

        #escribo el archivo con los compuestos alineados de acuerdo al indice de la base de datos
        for indice in range ( 1 , i ):
            fila = obtener_fila (connection , cursor , indice)
            archivo.write(fila + "\n")
        archivo.close()


        borrar_tabla_temporal(connection , cursor)
        

        time3 = time.time()
        tiempo_ejecucion_proceso = time3 - time1
        
        last_oid_proceso = select_max_oid_result_process(connection, cursor)

        guardar_info_proces(connection, cursor, last_oid_proceso, tiempo_ejecucion_alineamiento, tiempo_ejecucion_proceso, intervalo_time, min_range_accepted, min_porcent_range, max_porcent_range, file_destino, num_alineaciones)

        # una vez finalizado todo el proceso, cierro conexión con la BD
        print("**********fin de un una combinacion**************")

    except Exception as e:
        error_msg = str(e)
        print (error_msg)
        logging.error(error_msg)
        logging.exception("*exceptionAC*")
        #logging.exception(error_msg)
        #print("****fgdfgdf****")
        #print (error_msg)
        #close_connection(connection)
#        #cuando se cae el programa no funciona utilizar la misma conexión
#        connection = get_base_connection('postgres', 'postgres', 'admin')
#        cursor = get_cursor(connection)
#        borrar_tabla_temporal(connection , cursor)
#        close_connection(connection)

        #Poner alerta
        #messagebox.showerror("Alert" , "Something happened, please run the aplication again or call IT department")





#función principal, recibe la ruta del directorio de archivos de compuestos, ruta de archivos de matrices, rango de tiempo de medición, nombre del archivo de destino
def GraphPorcent(path_porc, path_mat, path_dest , intervalo_time, nombre_destino):
    # obtengo conexión
    connection = get_base_connection('postgres' , 'postgres' , 'admin')
    #obtengo cursor
    cursor = get_cursor(connection)

    try:
        #lista de nombres de archivos de porcentajes del directorio pasado por parámetro
        porcentaje_names = GetNamesDirectorio(path_porc)

        #get minimum retention time from first lines of all documents
        min_ret_time = min_retention_time(path_porc, porcentaje_names)
        
        #voy a recoger los elementos que caigan en este rango, comienza de 0
        contador_minutos = min_ret_time
        
        i = 1
        contador_archivos = 0

        #de 0 a 30 minutos
        #while (contador_minutos <= 30):
        print("rango: min: " + str(contador_minutos - intervalo_time) + " -- max: "+str(contador_minutos))
        #    L_procesar = []
            #bandera para contar los archivos
        contador_archivos = 0

        for p in porcentaje_names:
            contador_archivos = contador_archivos + 1
            #bandera para determinar que sólo se escoja un elemento por archivo
            contador_lineas = 0
            for index, line in enumerate(open(path_porc + '/' + p)):  # validar desde donde comienza la data (23)
                #si lo pongo en un and no funciona
                if line != '\n':
                    #si lo pongo en un and no funciona
                    if line != ' \n':
                        #si el indice es la linea 23 y el retention_time es un número
                        if (index >= 22) and (is_number(line.split()[1]) == True):
                            #si el retention_time esta en el rango indicado
                            #if (float(line.split()[1]) < contador_minutos) and (float(line.split()[1]) >= (contador_minutos - rango)) :
                                #si es el primer elemento del archivo q estoy cogiendo (evita que se seleccionen 2 o mas elementos en cada retention_time
                            arg = pfile() #creo y doty memoria a un objeto pfile
                            arg.file_name = p #p[:10] #nombre dl archivo
                            arg.max_scan = float(line.split()[3]) #scan máximo
                            arg.retention_time = float(line.split()[1]) #retention_time
                            arg.retention_time_promedio = float(line.split()[1])
                            #introducir aquí el resto de valores
                            arg.peak = line.split()[0] #
                            arg.first_scan = line.split()[2]
                            arg.last_scan = line.split()[4]
                            arg.pk = line.split()[5]
                            arg.index_file = contador_archivos
                            if (valida_decima_posicion(line) == True): # si existe o no el nuemro que acompana al campo ty en essa linea
                                arg.ty = line.split()[6]
                                arg.peak_height = line.split()[7]
                                arg.corr_area = line.split()[8] #concentración
                                arg.corr_max = line.split()[9]
                                arg.por_tot = line.split()[10]
                            else:
                                arg.ty = ''
                                arg.peak_height = line.split()[6]
                                arg.corr_area = line.split()[7] #concentración
                                arg.corr_max = line.split()[8]
                                arg.por_tot = line.split()[9]


                            base_line = str(arg.index_file) + "," + str(arg.retention_time) + "," + str(arg.peak_height)
                             
                            guardar_linea(connection, cursor, 'NO USO', 'POR', i, base_line)
                            i += 1 

            # continuo con el siguiente rango
            #contador_minutos = contador_minutos + rango


        # Una vez terminado con los rangos, genero los archivos a partir de información de la BD
        archivo = open(path_dest + '/' + nombre_destino + 'csv', 'w')
        #cabecera del archivo
        linea_cabecera = crear_cabecera(len(porcentaje_names))
        #escribo la cabecera en el archivo
        archivo.write(linea_cabecera + "\n")

        #escribo el archivo con los compuestos alineados de acuerdo al indice de la base de datos
        for indice in range ( 1 , i ):
            fila = obtener_fila (connection , cursor , indice)
            archivo.write(fila + "\n")
        archivo.close()


        borrar_tabla_temporal(connection , cursor)
        # una vez finalizado todo el proceso, cierro conexión con la BD
        close_connection(connection)

        #Poner alerta
        messagebox.showinfo("Alert" , "The files were created successfully")

    except Exception as e:

        error_msg = str(e)
        print (error_msg)
        close_connection(connection)
        #cuando se cae el programa no funciona utilizar la misma conexión
        connection = get_base_connection('postgres', 'postgres', 'admin')
        cursor = get_cursor(connection)
        borrar_tabla_temporal(connection , cursor)
        close_connection(connection)

        #Poner alerta
        messagebox.showerror("Alert" , "Something happened, please run the aplication again or call IT department")