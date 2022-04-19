from sympy import *
import pandas as pd
import numpy as np
# import scipy as sc
import matplotlib.pyplot as plt

def agrupar_por_intervalos(datos, n) :
    # agrupa los datos en n Intervalos
    rango=(5*int(datos.min()/5),5*(int(datos.max()/5)+1))
    frecs, intervalos= np.histogram(datos, range=rango, bins=n)
    intervalos_latex="$"+r", ".join([latex(Interval.Ropen(intervalos[i],intervalos[i+1])) for i in range(len(intervalos)-1)])+"$"
    return frecs, intervalos, intervalos_latex

def percentil(tabla, k=50) :
    # percentil si cae en medio de dos valores, devuelve el punto medio
    t = tabla.where(tabla['F_i']/tabla['f_i'].sum()>=k/100).dropna()
    if t.iloc[0]['F_i']/tabla['f_i'].sum() == k/100 :
        return (t.iloc[0]['x_i']+t.iloc[1]['x_i'])/2
    else :
        return t.iloc[0]['x_i']

    # tabla.where(tabla['F_i']/tabla['f_i'].sum()>=k/100).dropna().iloc[0]['x_i']
    # return tabla.where(tabla['F_i']/tabla['f_i'].sum()>k/100).dropna().iloc[0]['x_i']

def analisis_agrupado(frecs=[], intervalos=[]):
    #x_i, f_i, F_i, r_i  = np.unique(datos),np.bincount(datos), cumfreq(datos, numbins=len(np.unique(datos)))[0].astype(int), np.multiply(relfreq(datos, numbins=len(np.unique(datos)))[0],100)

    # Tabla de Frecuencias

    tabla = pd.DataFrame({'L_i':intervalos[:-1], 'R_i':intervalos[1:] ,
                        'x_i': (intervalos[:-1]+intervalos[1:])/2,
                        'f_i':frecs,
                        'F_i':np.cumsum(frecs),
                        'h_i':frecs/np.sum(frecs),
                        # 'H_i':(np.unique(datos, return_counts=True)[1]/len(datos)).cumsum(),
    #                       # '%_i':np.unique(datos, return_counts=True)[1]*100/len(datos),
    #                       # '%A_i':(np.unique(datos, return_counts=True)[1]*100/len(datos)).cumsum(),
    #                       # 'xf':np.unique(datos, return_counts=True)[0]*np.unique(datos, return_counts=True)[1],
    #                       # 'x2f':np.unique(datos, return_counts=True)[0]**2*np.unique(datos, return_counts=True)[1],
                         }
                         )
                        # ).set_index('x_i')
    # tabla.reset_index(inplace=True)
    # tabla.loc['suma']=tabla.sum()
    # d = np.diff(np.unique(datos)).min()
    # left_of_first_bin = datos.min() - float(d)/2
    # right_of_last_bin = datos.max() + float(d)/2
    # fg, ax = plt.subplots()
    # plt.clf()
    # plt.hist(datos, np.arange(left_of_first_bin, right_of_last_bin + d, d), rwidth=0.9, cumulative = False)
    # plt.title("Diagrama de barras")

    dic=dict()
    dic['frecs']=frecs
    dic['intervalos']=intervalos
    dic['intervalos_latex']="$"+r", ".join([latex(Interval.Ropen(intervalos[i],intervalos[i+1])) for i in range(len(intervalos)-1)])+"$"
    # dic['datos']=datos
    dic['tabla']=tabla
    # dic['media']=datos.mean()
    # dic['figure']=fg
    # dic['moda']= tabla[:-1].iloc[tabla[:-1]['f_i'].idxmax(),:]['x_i']
    # dic['mediana']=percentil(tabla[:-1],50)
    # dic['rango']=tabla[:-1]['x_i'].max()-tabla[:-1]['x_i'].min()
    # dic['varianza']=(tabla[-1:]['x2f'][0]/tabla[-1:]['f_i'][0]-dic['media']**2)
    # dic['desviacion']=sqrt(dic['varianza'])
    # dic['texto_media'] = r' $\overline{x}=\dfrac{\Sigma{x_i f_i}}{N}=' \
    #     +r'\dfrac{'+ str(tabla.iloc[:-1,7].sum()) \
    #     +r'}{'+str(tabla.iloc[:-1,1].sum())+r'}='+ \
    #     str(tabla.iloc[:-1,7].sum()/tabla.iloc[:-1,1].sum())+r'$'
    # dic['texto_moda']=r' $Mo='+ \
    #     str(tabla[:-1].iloc[tabla[:-1]['f_i'].idxmax(),:]['x_i'])+r'$'
    # dic['texto_mediana']=r' $Me='+ \
    #     str(dic['mediana'])+r'$'
    # dic['texto_desviacion']=r'$\sigma=\sqrt{\dfrac{\Sigma{x_i^2 f_i}}{N}-\overline{x}^2}=' \
    #     +r'\sqrt{\dfrac{'+str(tabla[-1:]['x2f'][0])+r'}{'+str(tabla.iloc[:-1,1].sum())+'}-' \
    #     +str(dic['media'])+'^2}'+'=' \
    #     +str(sqrt((tabla[-1:]['x2f'][0]/tabla[-1:]['f_i'][0]-dic['media']**2)))+r'$'
    return  dic

def analisis_discreto(str_datos):
    datos = np.loadtxt(str_datos.split())
    datos = datos.astype(int)
    #x_i, f_i, F_i, r_i  = np.unique(datos),np.bincount(datos), cumfreq(datos, numbins=len(np.unique(datos)))[0].astype(int), np.multiply(relfreq(datos, numbins=len(np.unique(datos)))[0],100)

    # Tabla de Frecuencias

    tabla = pd.DataFrame({'x_i':np.unique(datos), 'f_i':np.unique(datos, return_counts=True)[1],
                          'F_i':np.unique(datos, return_counts=True)[1].cumsum(),
                          'h_i':np.unique(datos, return_counts=True)[1]/len(datos),
                          'H_i':(np.unique(datos, return_counts=True)[1]/len(datos)).cumsum(),
                          '%_i':np.unique(datos, return_counts=True)[1]*100/len(datos),
                          '%A_i':(np.unique(datos, return_counts=True)[1]*100/len(datos)).cumsum(),
                          'xf':np.unique(datos, return_counts=True)[0]*np.unique(datos, return_counts=True)[1],
                          'x2f':np.unique(datos, return_counts=True)[0]**2*np.unique(datos, return_counts=True)[1],
                         }
                        ).set_index('x_i')
    tabla.reset_index(inplace=True)
    tabla.loc['suma']=tabla.sum()
    d = np.diff(np.unique(datos)).min()
    left_of_first_bin = datos.min() - float(d)/2
    right_of_last_bin = datos.max() + float(d)/2
    fg, ax = plt.subplots()
    plt.clf()
    plt.hist(datos, np.arange(left_of_first_bin, right_of_last_bin + d, d), rwidth=0.9, cumulative = False)
    plt.title("Diagrama de barras")

    dic=dict()
    dic['datos']=datos
    dic['tabla']=tabla
    dic['figure']=fg
    dic['media']=datos.mean()
    dic['moda']= tabla[:-1].iloc[tabla[:-1]['f_i'].idxmax(),:]['x_i']
    dic['mediana']=percentil(tabla[:-1],50)
    dic['rango']=tabla[:-1]['x_i'].max()-tabla[:-1]['x_i'].min()
    dic['varianza']=(tabla[-1:]['x2f'][0]/tabla[-1:]['f_i'][0]-dic['media']**2)
    dic['desviacion']=sqrt(dic['varianza'])
    dic['texto_media'] = r' $\overline{x}=\dfrac{\Sigma{x_i f_i}}{N}=' \
        +r'\dfrac{'+ str(tabla.iloc[:-1,7].sum()) \
        +r'}{'+str(tabla.iloc[:-1,1].sum())+r'}='+ \
        str(tabla.iloc[:-1,7].sum()/tabla.iloc[:-1,1].sum())+r'$'
    dic['texto_moda']=r' $Mo='+ \
        str(tabla[:-1].iloc[tabla[:-1]['f_i'].idxmax(),:]['x_i'])+r'$'
    dic['texto_mediana']=r' $Me='+ \
        str(dic['mediana'])+r'$'
    dic['texto_desviacion']=r'$\sigma=\sqrt{\dfrac{\Sigma{x_i^2 f_i}}{N}-\overline{x}^2}=' \
        +r'\sqrt{\dfrac{'+str(tabla[-1:]['x2f'][0])+r'}{'+str(tabla.iloc[:-1,1].sum())+'}-' \
        +str(dic['media'])+'^2}'+'=' \
        +str(sqrt((tabla[-1:]['x2f'][0]/tabla[-1:]['f_i'][0]-dic['media']**2)))+r'$'
    return  dic
