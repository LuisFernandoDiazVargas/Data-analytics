########################################################################################################################
########################################### EXPLORACIÓN DE DATOS #######################################################
########################################################################################################################

#Importando ibrerías a usar

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as xp
import seaborn as sb
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


mes = ["2022-1", "2022-2", "2022-3", "2022-4", "2022-5", "2022-6", "2022-7", "2022-8", "2022-9", "2022-10", "2022-11", "2022-12"]
idx = 1
for i in mes:
    TortaMes = MCDETA1_2022[MCDETA1_2022["MES"]==i]["TIPO_GUIA"].value_counts()
    print(TortaMes)
    plt.subplot(2, 6, idx)
    plt.pie(TortaMes, autopct='%1.1f%%', textprops={'fontsize': 7})
    plt.title(i)
    idx+=1
plt.tight_layout()
plt.legend(TortaMes.index, loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=3)
plt.show()










