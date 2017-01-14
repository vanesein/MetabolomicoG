#!/usr/bin/python
#! -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


#filename3 = "C:\\Users\\vaneseinh\\Documents\\MCC\\TESIS MCC\\metabolomico\\resultados\\100 101_30_0.15\\procesos.csv"
#df3 = pd.read_csv(filename3)
#
#info3 = df3[[  'min_interval_confianza','max_interval_confianza','num_alineaciones']]
##print(info.head())
##print(info.dtypes)
##print(info.sample(n=5))
#
#info3.sort_values(by=['min_interval_confianza','max_interval_confianza', 'num_alineaciones'], ascending=True)
#
#
#g3 = info3.groupby(['min_interval_confianza','max_interval_confianza','num_alineaciones'], as_index=False)#.size().reset_index()
#
#plt.figure()
#plt.hold(True)
#for x in range(0.01,0.23):
	#k= info3.groupby(['min_interval_confianza']).get_group(x)
	#plt.plot(k['max_interval_confianza'],k1['num_alineaciones'], label='Int 100',color = 'b', linewidth = 2)
#
#
#
#
##fig.suptitle('test title')
#plt.xlabel("Max")
#plt.ylabel("# Alineaciones")
#plt.legend(loc='best')
#
##fig.savefig('test.jpg')
#plt.show()




filename2 = "C:\\Users\\vaneseinh\\Documents\\MCC\\TESIS MCC\\metabolomico\\resultados\\100 101_30_0.15\\procesos.csv"
df2 = pd.read_csv(filename2)

info2 = df2[['intervalo_time', 'intensidad_aceptacion', 'num_alineaciones']]
#print(info.head())
#print(info.dtypes)
#print(info.sample(n=5))

info2.sort_values(by=['intervalo_time','intensidad_aceptacion', 'num_alineaciones'], ascending=True)


g2 = info2.groupby(['intensidad_aceptacion','intervalo_time','num_alineaciones'], as_index=False)#.size().reset_index()
#print(g.head(10))
j1= info2.groupby(['intensidad_aceptacion']).get_group(100)
j2= info2.groupby(['intensidad_aceptacion']).get_group(101)

#print(i1.head(10))

#g = g.cumsum()
plt.figure()
plt.hold(True)
plt.plot(j1['intervalo_time'],j1['num_alineaciones'], label='Int 100',color = 'b', linewidth = 2)
plt.plot(j2['intervalo_time'],j2['num_alineaciones'], label='Int 101',color = 'r', linewidth = 2)

#fig.suptitle('test title')
plt.xlabel("RT")
plt.ylabel("# Alineaciones")
plt.legend(loc='best')

#fig.savefig('test.jpg')
plt.show()




filename = "C:\\Users\\vaneseinh\Documents\\MCC\TESIS MCC\\metabolomico\\resultados\\100 a algo_0.1_0.15 ok\\procesos.csv"
df = pd.read_csv(filename)

info = df[['intervalo_time', 'intensidad_aceptacion', 'num_alineaciones']]
#print(info.head())
#print(info.dtypes)
#print(info.sample(n=5))

info.sort_values(by=['intervalo_time','intensidad_aceptacion', 'num_alineaciones'], ascending=True)


g = info.groupby(['intensidad_aceptacion','intervalo_time','num_alineaciones'], as_index=False)#.size().reset_index()
#print(g.head(10))
i1= info.groupby(['intervalo_time']).get_group(0.1)
i2= info.groupby(['intervalo_time']).get_group(0.2)
i3= info.groupby(['intervalo_time']).get_group(0.3)
i4= info.groupby(['intervalo_time']).get_group(0.4)
i5= info.groupby(['intervalo_time']).get_group(0.5)
#print(i1.head(10))

#g = g.cumsum()
plt.figure()
plt.hold(True)
plt.plot(i1['intensidad_aceptacion'],i1['num_alineaciones'], label='RT 0.1',color = 'b', linewidth = 2)
plt.plot(i2['intensidad_aceptacion'],i2['num_alineaciones'], label='RT 0.2',color = 'g', linewidth = 2)
plt.plot(i3['intensidad_aceptacion'],i3['num_alineaciones'], label='RT 0.3',color = 'r', linewidth = 2)
plt.plot(i4['intensidad_aceptacion'],i4['num_alineaciones'], label='RT 0.4',color = 'y', linewidth = 2)
plt.plot(i5['intensidad_aceptacion'],i5['num_alineaciones'], label='RT 0.5',color = 'm', linewidth = 2)

#fig.suptitle('test title')

plt.xlabel("Intesidad")
plt.ylabel("# Alineaciones")
plt.legend(loc='best')
#fig.savefig('test.jpg')
plt.show()




