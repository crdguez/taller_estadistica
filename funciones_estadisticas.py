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
                        'H_i':np.cumsum(frecs)/np.sum(frecs),
                        '%_i':frecs*100/np.sum(frecs),
                        '%A_i':np.cumsum(frecs)*100/np.sum(frecs),
                        'xf':(intervalos[:-1]+intervalos[1:])/2*frecs,
                        'x2f':((intervalos[:-1]+intervalos[1:])/2)**2*frecs,
                         }
                         )
                        # ).set_index('x_i').reset_index(inplace=True)
    tabla.loc['suma']=tabla.sum()


    # d = np.diff(np.unique(datos)).min()
    # left_of_first_bin = tabla[:-1]['L_i'].min()
    #
    # right_of_last_bin = tabla[:-1]['R_i'].max()
    # d=(right_of_last_bin-left_of_first_bin)/len(intervalos)
    fg, ax = plt.subplots()
    plt.clf()

    # plt.bar([1,2,3], [1,4,6])


    # plt.barh(xx, yy)
    # xx = tabla['x_i'][:-1]
    # yy = tabla['f_i'][:-1]
    # plt.barh(yy, xx)
    # plt.show()

    # plt.hist(datos, np.arange(left_of_first_bin, right_of_last_bin + d, d), rwidth=0.9, cumulative = False)
    # plt.hist([np.repeat(intervalos,frecs)], intervalos )
    plt.hist(np.repeat((intervalos[:-1]+intervalos[1:])/2,frecs), intervalos, rwidth=0.99 )
    plt.title("Histograma")

    dic=dict()
    dic['frecs']=frecs
    dic['intervalos']=intervalos
    dic['intervalos_latex']="$"+r", ".join([latex(Interval.Ropen(intervalos[i],intervalos[i+1])) for i in range(len(intervalos)-1)])+"$"
    # dic['datos']=datos
    dic['tabla']=tabla
    # dic['media']=datos.mean()
    dic['figure']=fg
    dic['media']=tabla.iloc[:-1,9].sum()/tabla.iloc[:-1,3].sum()


    t=tabla[:-1]
    indice_modal=t['f_i'].idxmax()
    f=t.iloc[indice_modal]
    dic['intervalo_modal']=f
    fa=t.iloc[indice_modal-1]
    fp=t.iloc[indice_modal+1]
    # fila_intervalo_modal=tabla.iloc[tabla.iloc[:-1]['f_i'].idxmax()]
    dic['moda']=str(f['L_i']+(f['f_i']-fa['f_i'])*(f['R_i']-f['L_i'])/((f['f_i']-fa['f_i'])+f['f_i']-fp['f_i']))


    k=50
    N=t['f_i'].sum()
    f=t.where(t['F_i']/t['f_i'].sum()>=k/100).dropna().iloc[0]
    dic['intervalo_mediana']=f
    dic['mediana']=str(f['L_i']+(f['R_i']-f['L_i'])*(k*N/100-(f['F_i']-f['f_i']))/f['f_i'])

    # dic['moda']= tabla[:-1].iloc[tabla[:-1]['f_i'].idxmax(),:]['x_i']
    # dic['mediana']=percentil(tabla[:-1],50)
    # dic['rango']=tabla[:-1]['x_i'].max()-tabla[:-1]['x_i'].min()
    dic['varianza']=(tabla[-1:]['x2f'][0]/tabla[-1:]['f_i'][0]-dic['media']**2)
    dic['desviacion']=sqrt(dic['varianza'])
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


def  analisis_bidimensional(datos, var1='x', var2='y'):
#     Recibe un numpy array de datos con dos columnas, la primera la interpreta como x y la segunda como y. Devuelve un diccionario con la información del análisis de regresión

    tabla = pd.DataFrame({var1: datos[:,0], var2: datos[:,1]})
    numero_datos=tabla.shape[0]

    tabla2 =tabla
    tabla2=tabla2.join(pd.DataFrame({'$'+var1+r'\cdot '+var2+r'$':datos[:,0]*datos[:,1],r'$'+var1+r'^2$':datos[:,0]**2, r'$'+var2+r'^2$':datos[:,1]**2}))
    tabla2.loc['Sumas']=tabla2.sum()
    tabla2.loc['Medias']=tabla2.iloc[:-1].mean()
    tabla2

    # Medias
    m1, m2 = [tabla2.loc[tabla2.index[-2]][c]/numero_datos for c in range(2)]
    medias=[m1,m2]

    vari =[var1, var2]

    latex_medias =r'Medias: '
    for c in range(2) :
        latex_medias += r"$\overline{"+tabla.columns[c]+r"}=\dfrac{\Sigma{"+vari[c]+r"_i}}{N}="+ \
        r"\dfrac{"+str(tabla2.loc[tabla2.index[-2]][c])+ \
        r"}{"+latex(numero_datos)+r"}="+latex(tabla2.loc[tabla2.index[-2]][c]/numero_datos)+"$. "

    latex_centro = r'El centro de gravedad es: $('+latex(m1)+r','+latex(m2)+')$'

    # Desviaciones típicas y covarianza
    s1, s2 = [sqrt(tabla2.loc[tabla2.index[-2]][c+3]/numero_datos-medias[c]**2) for c in range(2)]
    sxy=tabla2.loc[tabla2.index[-2]][2]/numero_datos-m1*m2
#     display(s1,s2,sxy)

    latex_varianzas = r'Varianzas y covarianzas: '+ \
    r' $\sigma_'+var1+r'=\sqrt{\frac{\sum{'+var1+r'_i^2}}{N}-\overline{'+var1+r'}^2}=\sqrt{\frac{'+latex(tabla2.loc[tabla2.index[-2]][3])+r'}{'+ \
    latex(numero_datos)+r'}-'+latex(medias[0])+r'^2}='+latex(s1)+r'$.' + \
    r' $\sigma_'+var2+r'=\sqrt{\frac{\sum{'+var2+r'_i^2}}{N}-\overline{'+var2+r'}^2}=\sqrt{\frac{'+latex(tabla2.loc[tabla2.index[-2]][4])+r'}{'+ \
    latex(numero_datos)+r'}-'+latex(medias[1])+r'^2}='+latex(s2)+r'$.'+ \
    r' $\sigma_{'+var1+var2+r'}=\frac{\sum{'+var1+r'_i \cdot '+var2+r'_i}}{N}-\overline{'+var1+r'}\cdot \overline{'+var2+r'}=\frac{'+latex(tabla2.loc[tabla2.index[-2]][2])+r'}{'+ \
    latex(numero_datos)+r'}-'+latex(medias[0])+r'\cdot '+latex(medias[1])+r'='+latex(sxy)+r'$.'


    latex_correlacion = r'Correlación: '+ \
    r'$r=\dfrac{\sigma_{'+var1+var2+r'}}{\sigma_'+var1+r' \cdot \sigma_'+var2+r'}=\dfrac{'+latex(sxy)+r'}{'+ \
    latex(s1)+r'\cdot '+latex(s2)+r'}='+latex(sxy/(s1*s2))+r'$.'
#
#     pendiente, ordenada, coefcorr = stats.linregress(datos)[:3]
# #   display(pendiente, ordenada, coefcorr, Eq(y,pendiente*x+ordenada))
#

    pendiente = sxy/s1**2
    ordenada = m2-m1*sxy/s1**2
    recta= Eq(S('y'),pendiente*S('x')+ordenada)
    latex_recta = r'Recta de regresión: La pendiente es: '+latex(pendiente)+r', la ordenada en el origen: '+latex(ordenada) \
                +r', El coeficiente de correlación:'+latex(sxy/(s1*s2)) \
                +r' y la recta de regresión: $'+latex(recta)+r'$'

    # p=plot_implicit(Eq(y,exp), (x, -10, 10), (y, -10, 10))
    p=plot_implicit(recta, ('x',tabla['x'].min()*0.6,tabla['x'].max()*1.3), ('y',tabla['y'].min()*0.6,tabla['y'].max()*1.3),axis_center=(0,0))

    fg, ax = p._backend.fig, p._backend.ax
    ax[0].set_title("$y="+latex(nsimplify(pendiente*S('x')+ordenada))+"$  \n ")
    # ax[0].set_aspect('equal')
    plt.scatter(tabla['x'],tabla['y'])
    plt.grid(True)

    dic=dict()

    dic['datos']=datos
    dic['tabla_ini']=tabla
    # dic['tabla_ini_latex']=tabulate(tabla, headers="keys", tablefmt="latex",showindex = False).replace('\\$','$').replace('textbackslash{}','')
    # dic['tabla_fin_latex']=tabulate(tabla2, headers="keys", tablefmt="latex",showindex = True).replace('\\$','$').replace('textbackslash{}','').replace('\^{}','^')
    tabla2.index = tabla2.index.map(str)
    dic['tabla_fin']=tabla2.style.highlight_max(axis=0)
    dic['latex_medias']=latex_medias
    dic['latex_centro']=latex_centro
    dic['latex_varianzas']=latex_varianzas
    dic['latex_correlacion']=latex_correlacion
    dic['latex_recta']=latex_recta
    dic['recta']=recta
    dic['fg']=fg
    # dic['latex']=latex_sol
    # dic['figura']=sns.regplot(x=datos[:,0],y=datos[:,1]).figure

    return dic
