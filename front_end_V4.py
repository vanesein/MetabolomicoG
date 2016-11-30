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

#from tkinter import *
#from tkinter import filedialog
#from tkinter import messagebox
from archivos_cibe_V7 import MainProcess
from archivos_cibe_V7 import GraphPorcent
from conect_trans import *

# obtiene los nombres de los archivos en un directorio
def GetNamesDirectorio( path_dir):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path_dir):
        f.extend(filenames)
        break
    return f

if __name__ == "__main__":
    dir_porcentajes = os.getcwd()+'/test_data/porcentaje'
    dir_matrices = os.getcwd()+'/test_data/matrices'
    dir_destino = os.getcwd()+'/test_data'

    #lista de nombres de archivos de porcentajes del directorio pasado por parámetro
    porcentaje_names = GetNamesDirectorio(dir_porcentajes)
    #lista de nombres de archivos de matriz del directorio pasado por parámetro
    matriz_names = GetNamesDirectorio(dir_matrices)


    #min_porcent_range, max_porcent_range
    #intervalo_time, nombre_destino, min_range_accepted,
    #min_range_accepted HASTA 5000

    # obtengo conexión
    connection = get_base_connection('postgres' , '' , 'admin')
    #obtengo cursor
    cursor = get_cursor(connection)

    intervalo_time = 0.1
    min_interval_confianza = 0.01
    max_interval_confianza = 0.01
    intensidad_aceptacion = 100
    file_destino = 'align'

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
    
    #MainProcess(dir_porcentajes, dir_matrices, dir_destino, intervalo_time, file_destino, intensidad_aceptacion, min_interval_confianza, max_interval_confianza)
    close_connection(connection)





