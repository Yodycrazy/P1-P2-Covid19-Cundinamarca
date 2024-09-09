# -*- coding: utf-8 -*-
"""P1_proyecto.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GxO9ZKEi4DV-ko-8PdSvQOG1s6KdJVYL

Casos positivos de COVID-19 en Colombia.
cundinamarca
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

df = pd.read_csv("/content/Casos_positivos_de_COVID-19_en_Colombia..csv")
df

df.columns

df['Nombre municipio']

df['Fecha de muerte']

df.dtypes #Ver tipos de datos existentes en la base

df.iloc[100] #filtar el registro 100

df.info() #Ver información general

"""Analisis de nulos"""

#valor faltante .,:; por NaN
# NaN = Not a Number
import numpy as np
df.replace('.',np.nan,inplace=True)
df.tail()

df.isna().sum().sort_values(ascending = False) #Revisar la cantidad de valores SUCIOS de la base

"""Conclusiones:
* Nombre del país, Código ISO del país, Nombre del grupo étnico, Fecha de muerte, Tipo de recuperación y Fecha de recuperación tienen demasiados nulos --> eliminar Variables
* Estado, Ubicación del caso, Recuperado, Fecha de inicio de síntomas, Fecha de diagnóstico y Pertenencia étnica --> imputarlos tras EDA

"""

df.drop(columns = ['Nombre del país','Código ISO del país'], inplace = True)
df

df.drop(columns = ['Nombre del grupo étnico','Fecha de muerte'], inplace = True)
df

df.drop(columns = ['Tipo de recuperación','Fecha de recuperación'], inplace = True)
df

df.columns

df.isna().sum().sort_values(ascending = False) #Revisar la cantidad de valores SUCIOS de la base

df['Pertenencia étnica']

"""Analisis de exploración de datos EDA
Variables categoricas (no numerico)
"""

def graficos_eda_categoricos(cat):

    #Calculamos el número de filas que necesitamos
    from math import ceil
    filas = ceil(cat.shape[1] / 2)

    #Definimos el gráfico
    f, ax = plt.subplots(nrows = filas, ncols = 2, figsize = (16, filas * 6))

    #Aplanamos para iterar por el gráfico como si fuera de 1 dimensión en lugar de 2
    ax = ax.flat

    #Creamos el bucle que va añadiendo gráficos
    for cada, variable in enumerate(cat):
        cat[variable].value_counts().plot.barh(ax = ax[cada])
        ax[cada].set_title(variable, fontsize = 12, fontweight = "bold")
        ax[cada].tick_params(labelsize = 12)

graficos_eda_categoricos(df.select_dtypes('O'))

"""Conclusiones:
Nombre departamento solo tiene un valor --> eliminarla
Pertenencia étnica no aporta info importante --> eliminarla

Sobre las imputaciones pendientes:
Estado : imputar por Leve
Ubicacion del caso : imputar por Casa
Recuperado : imputar por Fallecido
"""

df.drop(columns = ['Nombre departamento', 'Pertenencia étnica'], inplace = True)
df

df['Estado'] = df['Estado'].fillna('Leve')

df['Ubicación del caso'] = df['Ubicación del caso'].fillna('Casa')

df['Recuperado'] = df['Recuperado'].fillna('Fallecido')

df.isna().sum().sort_values(ascending = False) #Revisar la cantidad de valores SUCIOS de la base

df['Fecha de inicio de síntomas']

df['Fecha de diagnóstico'].unique()

"""conclusion:
'Fecha de inicio de síntomas' y 'Fecha de diagnóstico' son fechas iguales eliminar 1
"""

df.drop(columns = 'Fecha de inicio de síntomas', inplace = True)
df

df.isna().sum().sort_values(ascending = False) #Revisar la cantidad de valores SUCIOS de la base

"""#### EDA VARIABLES NUMÉRICAS

"""

def estadisticos_cont(num):
    #Calculamos describe
    estadisticos = num.describe().T
    #Añadimos la mediana
    estadisticos['median'] = num.median()
    #Reordenamos para que la mediana esté al lado de la media
    estadisticos = estadisticos.iloc[:,[0,1,8,2,3,4,5,6,7]]
    #Lo devolvemos
    return(estadisticos)

estadisticos_cont(df.select_dtypes('number'))

"""conclusiones:

Código DIVIPOLA departamento y Unidad de medida de edad: solo tienen un valor Eliminarlas
"""

df.drop(columns = ['Código DIVIPOLA departamento','Unidad de medida de edad'], inplace = True)
df

df.dtypes #Ver tipos de datos existentes en la base

clean_df  =df.copy() #Hacer una copia de la base hasta acá
clean_df2 = df.copy() #Crear una segunda base de datos y copiar los cambios realizados

clean_df

clean_df.dropna(inplace=True) #Reemplazar valores en la base de datos

np.sum(clean_df.isna()), clean_df.shape #Limpiar BD 0 errores

clean_df2.dropna(inplace=True) #limpiar BD 2 datos sucios 0
np.sum(clean_df2.isna()), clean_df2.shape

cols = list(clean_df.select_dtypes(include=['object']).columns)
cols

cols2 = list(clean_df2.select_dtypes(include=['object']).columns)
cols2

df.to_csv('data_covid.csv') #Exportar base de datos limpia

"""GENERACIÓN DE INSIGHTS"""

df['Estado'] = df['Estado'].str.capitalize()
df['Recuperado'] = df['Recuperado'].str.capitalize()

df.Recuperado.value_counts(normalize = True) * 100

df.Estado.value_counts(normalize = True) * 100

df.to_csv('data_covid1.csv') #Exportar base de datos limpia

df['Ubicación del caso'] = df['Ubicación del caso'].str.capitalize()

df['Ubicación del caso']

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

ax = sns.boxplot(data=df,x='Edad',y='Nombre municipio')
ax.set_ylim(0,20)

ax = sns.boxplot(data=df,x='Estado',y='Edad')
ax.set_ylim(0,100)

ax = sns.boxplot(data=df,x='Recuperado',y='Nombre municipio')
ax.set_ylim(0,30)