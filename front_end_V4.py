#!/usr/bin/python
#! -*- coding: utf-8 -*-

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


#'''--------------------------------------------------------------
#Autor: Isaac Torres Bermeo
#Afiliación: Centro de Visión y Robótica
#Versión: 7
#
#'''-------------------------------------------------------------
#''

import os

#import threading
#from queue import Queue

#from tkinter import *
#from tkinter import filedialog
#from tkinter import messagebox

from settings import *

from archivos_cibe_V7 import MainProcess
from conect_trans import *


#def do_work(connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza):
#    with lock:
#        MainProcess(connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza)
#
## The worker thread pulls an item from the queue and processes it
#def worker():
#    while True:
#        items = q.get()
#        do_work(items[0], items[1], items[2],items[3],items[4],items[5],items[6],items[7],items[8],items[9],items[10],items[11])
#        q.task_done()



# obtiene los nombres de los archivos en un directorio
def GetNamesDirectorio( path_dir):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path_dir):
        f.extend(filenames)
        break
    return f

if __name__ == "__main__":

    
    logging.info('***** Started *****')

    #lista de nombres de archivos de porcentajes del directorio pasado por parámetro
    porcentaje_names = GetNamesDirectorio(dir_porcentajes)
    #lista de nombres de archivos de matriz del directorio pasado por parámetro
    matriz_names = GetNamesDirectorio(dir_matrices)

    print(dir_porcentajes)
    print(dir_matrices)
    print(dir_destino)

    try:
        # obtengo conexión
        connection = get_base_connection('postgres' , 'postgres' , '')
        #obtengo cursor
        cursor = get_cursor(connection)

        # lock to serialize console output
        #lock = threading.Lock()
        if opc_run==1 :
            file_destino = 'align1'
            MainProcess(connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza)

        elif opc_run==2:
            for intensidad_aceptacion in range(100,5001):
                
                intervalo_time = 0.1
                while(intervalo_time<=30):
  
                    file_destino = 'align_'+str(intervalo_time)+'_'+str(intensidad_aceptacion)+'_'+str(min_interval_confianza)+'_'+str(max_interval_confianza)
        
                    MainProcess(connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza)

                    intervalo_time = round(intervalo_time + 0.1,2)

        else:
            for intensidad_aceptacion in range(100,5000):
                
                intervalo_time = 0.1
                while(intervalo_time<=30):
                    
                    min_interval_confianza = 0.01
                    while(min_interval_confianza<=1):
        
                        max_interval_confianza = 0.01
                        while(max_interval_confianza<=1):
                        
                            file_destino = 'align_'+str(intervalo_time)+'_'+str(intensidad_aceptacion)+'_'+str(min_interval_confianza)+'_'+str(max_interval_confianza)
        
                            MainProcess(connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza)
                        
                            max_interval_confianza = round(max_interval_confianza + 0.01,2)
        
                        min_interval_confianza = round(min_interval_confianza + 0.01,2)
        
                    intervalo_time = round(intervalo_time + 0.1,2)
        

        # Create the queue and thread pool.
#        q = Queue()
#        for i in range(4):
#             t = threading.Thread(target=worker)
#             t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
#             t.start()
#
#        for intensidad_aceptacion in range(100,103):
        
#            q.put((connection, cursor, dir_porcentajes, dir_matrices, porcentaje_names, matriz_names, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza))
#
#        q.join()       # block until all tasks are done


        close_connection(connection)

        logging.info('Finished')

    except Exception as e:
        error_msg = str(e)
        print (error_msg)
        logging.error(error_msg)
        logging.exception("*exceptionFE*")
        close_connection(connection)





