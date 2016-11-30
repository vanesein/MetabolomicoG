import os
import 	logging

global dir_porcentajes
global dir_matrices
global dir_destino

global intervalo_time
global min_interval_confianza
global max_interval_confianza
global intensidad_aceptacion

logging.basicConfig(filename='alineamiento.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

dir_porcentajes = os.getcwd()+'/test_data/porcentaje'
dir_matrices = os.getcwd()+'/test_data/matrices'
dir_destino = os.getcwd()+'/test_data'


#min_porcent_range, max_porcent_range
#intervalo_time, nombre_destino, min_range_accepted,
#min_range_accepted HASTA 5000
intervalo_time = 0.1
min_interval_confianza = 0.01
max_interval_confianza = 0.01
intensidad_aceptacion = 100

