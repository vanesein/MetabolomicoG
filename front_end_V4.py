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

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from archivos_cibe_V7 import MainProcess
from archivos_cibe_V7 import GraphPorcent
from conect_trans import *


class Application (Frame):

    def __init__ (self , master) :
        Frame.__init__(self , master)
        self.grid()
        #self.button_clicks = 0
        self.create_widgets()

    def create_widgets(self):

        self.label_principal = Label(self , text = "Software for files \ncorrection")
        self.label_principal.grid(row = 0 , column = 1  , sticky = W)
        #self.label_principal.place(relx=0.5 , rely=0.5 )

        self.dir_1 = Label(self , text = "Choose percent directory")
        self.dir_1.grid( row = 3 , column = 0  , sticky = W)
        #self.dir_1.place( x=30 , y = 20)

        self.dir_1_path = Entry(self)
        self.dir_1_path.grid( row = 3 , column = 1 , sticky = W)
        #self.dir_1_path.place( x=40 , y=20)

        self.submit_dir_1 = Button(self , text = "...." , command = self.reveal_dir1)
        self.submit_dir_1.grid(row = 3 , column = 2 , sticky = W)
        #self.submit_dir_1.place(x=50 , y=20)

        self.dir_2 = Label(self , text = "Choose fragments directory")
        self.dir_2.grid( row = 5 , column = 0  , sticky = W)
        #self.dir_1.place( x=30 , y = 20)

        self.dir_2_path = Entry(self)
        self.dir_2_path.grid( row = 5 , column = 1 , sticky = W)
        #self.dir_1_path.place( x=40 , y=20)

        self.submit_dir_2 = Button(self , text = "...." , command = self.reveal_dir2)
        self.submit_dir_2.grid(row = 5 , column = 2 , sticky = W)
        #self.submit_dir_1.place(x=50 , y=20)


        self.dir_3 = Label(self , text = "Choose output directory")
        self.dir_3.grid( row = 8 , column = 0  , sticky = W)
        #self.dir_1.place( x=30 , y = 20)

        self.dir_3_path = Entry(self)
        self.dir_3_path.grid( row = 8 , column = 1 , sticky = W)
        #self.dir_1_path.place( x=40 , y=20)

        self.submit_dir_3 = Button(self , text = "...." , command = self.reveal_dir3)
        self.submit_dir_3.grid(row = 8 , column = 2 , sticky = W)

        #self.text = Text(self , width = 35 , height = 5 , wrap = WORD)
        #self.text.grid(row = 3 , column = 0 , columnspan = 2 , sticky = W)

        self.submit_button = Button(self , text = "Proccess" , command = self.submit)
        self.submit_button.grid(row = 9 , column = 1 , sticky = W)

        #self.submit_button = Button(self , text = "Graph %" , command = self.graph_p)
        #self.submit_button.grid(row = 9 , column = 2 , sticky = W)

        self.submit_button = Button(self , text = "Cancel" , command = self.cancel)
        self.submit_button.grid(row = 9 , column = 2 , sticky = W)


    def reveal_dir1(self):

        dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        self.dir_1_path.delete(0,END)
        self.dir_1_path.insert(0,dirname)


    def reveal_dir2(self):

        dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        self.dir_2_path.delete(0,END)
        self.dir_2_path.insert(0,dirname)


    def reveal_dir3(self):

        dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        self.dir_3_path.delete(0,END)
        self.dir_3_path.insert(0,dirname)


    # obtiene los nombres de los archivos en un directorio
    def GetNamesDirectorio(self, path_dir):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(path_dir):
            f.extend(filenames)
            break
        return f

    def submit(self):
        #dirname = filedialog.askdirectory(parent=root , initialdir="/" , title="fxddfgdg")
        #MainProcess(self.dir_1_path.get() , self.dir_2_path.get() , self.dir_3_path.get() , 0.1 , 'align.')

        dir_porcentajes = os.getcwd()+'/test_data/porcentaje'
        dir_matrices = os.getcwd()+'/test_data/matrices'
        dir_destino = os.getcwd()+'/test_data'

        #lista de nombres de archivos de porcentajes del directorio pasado por parámetro
        porcentaje_names = self.GetNamesDirectorio(dir_porcentajes)
        #lista de nombres de archivos de matriz del directorio pasado por parámetro
        matriz_names = self.GetNamesDirectorio(dir_matrices)


        #min_porcent_range, max_porcent_range
        #intervalo_time, nombre_destino, min_range_accepted,
        #min_range_accepted HASTA 5000

        # obtengo conexión
        connection = get_base_connection('postgres' , 'postgres' , 'admin')
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

        messagebox.showinfo("Alert" , "ALL files were created successfully")
        self.quit()

    



    def graph_p(self):
        #dirname = filedialog.askdirectory(parent=root , initialdir="/" , title="fxddfgdg")
        #MainProcess(self.dir_1_path.get() , self.dir_2_path.get() , self.dir_3_path.get() , 0.1 , 'align.')
        MainProcess('C:/Users/vaneseinh/Documents/MCC/TESIS MCC/metabolomico/test_data/porcentaje' , 'C:/Users/vaneseinh/Documents/MCC/TESIS MCC/metabolomico/test_data/matrices' , 'C:/Users/vaneseinh/Documents/MCC/TESIS MCC/metabolomico/test_data' , 0.1 , 'align.')
        self.quit()


    def cancel(self):

        #dirname = filedialog.askdirectory(parent=root , initialdir="/" , title = "fdf")
        self.quit()






        #self.button = Button(self)
        #self.button["text"] = "Total Clicks: 0"
        #self.button["command"] = self.update_count
        #self.button.grid()

    #def update_count(self):
     #   self.button_clicks += 1
     #   self.button["text"] = "Total Clicks: " + str(self.button_clicks)



root = Tk()

root.title("Sistema de correcion de archivos")
root.geometry("500x500")

app = Application(root)





root.mainloop()



