########################################################################################################################
########################################### EXPLORACIÓN DE DATOS #######################################################
########################################################################################################################

#Importando ibrerías a usar

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#Importando Excel
MCDETA=pd.read_excel("C:/Users/asus/Desktop/POSTAL.xlsx")

#Extrayendo columnas importantes
MCDETA1=MCDETA[["FEC_TRANSMISION", "TIPO_GUIA", "NUMCON", "NUMCONM", "FOB_CONO"]]

#Creando nueva columna "MES" y de "DIA"
MCDETA1["MES"] = MCDETA1["FEC_TRANSMISION"].dt.to_period("M")
MCDETA1["DIA"] = MCDETA1["FEC_TRANSMISION"].dt.to_period("D")
print(MCDETA1)

#Verificando valores NULL
print(MCDETA1.isnull().sum())

#Verificando los tipos de datos
print(MCDETA1.dtypes)

#Mostrando solo 2022
MCDETA1_2022 = MCDETA1[(MCDETA1["FEC_TRANSMISION"] >= '2022-01-01') &
                       (MCDETA1["FEC_TRANSMISION"] < '2023-01-01')]

#Limpiando la data quitando los DPO's que terminaron en XX que fueron error de manifiesto
MCDETA_XX = MCDETA1_2022[MCDETA1_2022["NUMCONM"].str.endswith("XX")]
MCDETA1_2022 = MCDETA1_2022[~MCDETA1_2022["NUMCONM"].str.endswith("XX")]
print(MCDETA_XX)

print("EL NUMERO DE MERCANCÍAS CON ERRORES DE MANIFIESTO ES",
      len(MCDETA_XX)
      )

#Reseteando indices (Esencial para sincronizar el índice despues de sustraer o añadir filas)
MCDETA1_2022 = MCDETA1_2022.reset_index(drop=True)
print(MCDETA1_2022)

#Tabla Pivot de FOB por MES según Tipo de servicio
MCDETA1_2022_PIVOT = MCDETA1_2022.pivot_table(index="MES",
                                              columns="TIPO_GUIA",
                                              values="FOB_CONO",
                                              aggfunc='sum'
                                              )
print(MCDETA1_2022_PIVOT)
print(MCDETA1_2022_PIVOT.dtypes)


#Grafico 1: FOB POR MES SEGÚN TIPO DE SERVICIO
MCDETA1_2022_PIVOT.plot(kind = "line")
plt.title("FOB POR MES SEGUN TIPO DE SERVICIO")
plt.show()

#Grafico 2: Cantidad de envíos transmitidos por dia
Grupo=MCDETA1_2022.groupby("DIA").size()
Grupo.plot(kind="line")
plt.show()

#Resumen estadístico
print(MCDETA1_2022.describe())

#Mostrando el maximo y minimo valor
#En pandas, en un Data Frame agrupado por grpuppby el indice es la columna agrupada
print("El dia que tuvo mas envíos transmitidos fue: ", Grupo.idxmax(), ": ", Grupo.max())
print("El dia que tuvo menos envíos transmitidos fue: ", Grupo.idxmin(), ": ", Grupo.min())

#Como ya reseteamos el indice, loc y iloc no tendran problemas y darán el mismo resultado
#Ahora obtenemos el envío con mayor FOB transmitido en 2022
print("El envío con mayor FOB fue: ", MCDETA1_2022.iloc[MCDETA1_2022["FOB_CONO"].idxmax()])

#Cuando un mercancía supera los 200 dólares tributa.
#Obteniendo las mercanías que tributan
MCDETA1_2022["TRIBUTO"]=np.where(MCDETA1_2022["FOB_CONO"]>200, "SÍ", "NO")
print(MCDETA1_2022)

#Grafico multiple
mes = pd.Series(MCDETA1_2022_PIVOT.index)
MesNombre =["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
idx = 1
fig = plt.figure(figsize=(10,5))
fig.suptitle('Tipos de servicio por mes', fontsize=16)
for i in mes:
    TortaMes = MCDETA1_2022[MCDETA1_2022["MES"]==i]["TIPO_GUIA"].value_counts()
    plt.subplot(2, 6, idx)
    plt.pie(TortaMes, autopct='%1.1f%%', textprops={'fontsize': 8})
    plt.title(MesNombre[idx-1])
    idx+=1
plt.tight_layout()
plt.legend(TortaMes.index, loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=3)
plt.show()

#Los envíos con valor FOB=0 son envíos que se mantienen notificados, es decir, no tienen levante.
#Para graficar el histograma tenemos
var=MCDETA1_2022[MCDETA1_2022["FOB_CONO"]>0]["FOB_CONO"]

#Obteniendo estadísticos
min_val = var.min()
max_val = var.max()
mean_val = var.mean()
med_val = var.median()
mod_val = var.mode()[0]

print('Minimum:{:.2f}\nMean:{:.2f}\nMedian:{:.2f}\nMode:{:.2f}\nMaximum:{:.2f}\n'.format(min_val,
                                                                                        mean_val,
                                                                                        med_val,
                                                                                        mod_val,
                                                                                        max_val))
#Creando la figura
fig = plt.figure(figsize=(10,4))
plt.hist(var, bins=5000)

#Agregando Lineas de los estadísticos
plt.axvline(x=min_val, color = 'gray', linestyle='dashed', linewidth = 2)
plt.axvline(x=mean_val, color = 'cyan', linestyle='dashed', linewidth = 2)
plt.axvline(x=med_val, color = 'red', linestyle='dashed', linewidth = 2)
plt.axvline(x=mod_val, color = 'yellow', linestyle='dashed', linewidth = 2)
plt.axvline(x=max_val, color = 'gray', linestyle='dashed', linewidth = 2)

#Agregando labels
plt.title('Data Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()










