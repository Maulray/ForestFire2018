#Proba réserve en eau du sol

import numpy as np
from random import*
from matplotlib.pyplot import matshow
import matplotlib.pylab as plt
import matplotlib.animation as animation
from time import*
from matplotlib import*
import math

def liste(p):
    '''prend en argument une probabilité p de passer de l'état arbre normal à arbre en feu, et renvoie une liste qui permet de piocher un 1 ou un 2 avec la bonne probabilité d'apparition'''
    #C'est pour le moment la meilleure piste que j'ai pour intégrer des probabilités
    a=math.floor(100*p)
    L=[]
    for i in range (0,a):
        L.append(2)
    for i in range (0,100-a):
        L.append(1)
    return L
    

#On travaille sur une matrice nxn mais on n'affiche qu'une matrice n-2xn-2 parce que les effets de bord ne sont pas contrôlés 
#On suppose que, sans autres effets extérieurs, la probabilité qu'un arbre prenne feu est de 0.8   

def proba(x):
    '''Prend un x POSITIF entre 0 et 1(exclu) modélisant la réserve en eau du sol en milimètres et renvoie la valeur de la probabilité que le feu se propage'''
    x=x/1000
    if x>=0.15:
        return 0
    elif x<=0.1:
        return 1
    return (math.log(math.sqrt((0.15+1)/(1-0.15)))-math.log(math.sqrt((x+1)/(1-x))))/(math.log(math.sqrt((0.15+1)/(1-0.15)))-math.log(math.sqrt((0.1+1)/(1-0.1))))
    

def crea_foret_feu(n):
    #Création forêt
    cmap1 = colors.ListedColormap(['white','limegreen'])
    cmap2=colors.ListedColormap(['white','limegreen','red'])
    anima=[]
    F=np.zeros((n,n),dtype=int)
    DF=0.8 #probabilité qu'il y ait un arbre sur 1m²
    for i in range(0,n):    #Création d'une matrice composée de 1(arbre) et de 0(vide) de façon aléatoire selon la probabilité DF
        for j in range(0,n):
            if random()<DF:
                F[i,j]=1
            else:
                F[i,j]=0 
    G=F[2:n-2,2:n-2]
    print (G)
    anima.append([matshow(G, fignum=False, animated=True, cmap=cmap1)])
    plt.draw() 
    plt.show()
    input()
    plt.close()
    #Mise en feu d'un arbre
    m=randint(1,n-2)
    r=randint(1,n-2)
    while F[m,r]!=1:
        m=randint(1,n-2)  
        r=randint(1,n-2)
    L=[(m,r)]
    F[m,r]=2
    G=F[2:n-2,2:n-2]
    print (G)
    anima.append([matshow(G, fignum=False, animated=True, cmap=cmap2)])
    
    plt.draw() 
    plt.show()
    return F,L
    
def propag(n,V,x):
    '''Prend en argument un format de matrice carrée, la provenance du vent à choisir parmi 'N', 'S', 'E', 'O', 'NE','NO', 'SO', 'SE', 'A', x la réserve en eau du sol en mm et renvoie la création d'une forêt, la mise en feu d'un arbre et la première étape de la propagation'''
    cmap = colors.ListedColormap(['white','limegreen','red','black'])
    anima=[]
    F,L=crea_foret_feu(n)
    input()
    plt.close()
    p=proba(x)
    P=liste(p)
    for (m,r) in L:
        if m<n-1 and r<n-1 and m>1 and r>1:
            if V=='S':#vent du sud
                if F[m-1,r-1]==1:
                    F[m-1,r-1]=choice(P)
                    if F[m-1,r-1]==2:
                        L.append((m-1,r-1))
                if F[m-1,r]==1:
                    F[m-1,r]=choice(P)
                    if F[m-1,r]==2:
                        L.append((m-1,r))
                if F[m-1,r+1]==1:
                    F[m-1,r+1]=choice(P)
                    if F[m-1,r+1]==2:
                        L.append((m-1,r+1))
            if V=='N':#vent du nord
                if F[m+1,r-1]==1:
                    F[m+1,r-1]=choice(P)
                    if F[m+1,r-1]==2:
                        L.append((m+1,r-1))
                if F[m+1,r]==1:
                    F[m+1,r]=choice(P)
                    if F[m+1,r]==2:
                        L.append((m+1,r))
                if F[m+1,r+1]==1:
                    F[m+1,r+1]=choice(P)
                    if F[m+1,r+1]==2:
                        L.append((m+1,r+1))
            if V=='E':#vent d'ouest
                if F[m-1,r-1]==1:
                    F[m-1,r-1]=choice(P)
                    if F[m-1,r-1]==2:
                        L.append((m-1,r-1))
                if F[m,r-1]==1:
                    F[m,r-1]=choice(P)
                    if F[m,r-1]==2:
                        L.append((m,r-1))
                if F[m+1,r-1]==1:
                    F[m+1,r-1]=choice(P)
                    if F[m+1,r-1]==2:
                        L.append((m+1,r-1))
            if V=='O':#vent d'est
                if F[m-1,r+1]==1:
                    F[m-1,r+1]=choice(P)
                    if F[m-1,r+1]==2:
                        L.append((m-1,r+1))
                if F[m,r+1]==1:
                    F[m,r+1]=choice(P)
                    if F[m,r+1]==2:
                        L.append((m,r+1))
                if F[m+1,r+1]==1:
                    F[m+1,r+1]=choice(P)
                    if F[m+1,r+1]==2:
                        L.append((m+1,r+1))
            if V=='SO':#vent du sud ouest
                if F[m-1,r+1]==1:
                    F[m-1,r+1]=choice(P)
                    if F[m-1,r+1]==2:
                        L.append((m-1,r+1))
                if F[m-1,r]==1:
                    F[m-1,r]=choice(P)
                    if F[m-1,r]==2:
                        L.append((m-1,r))
                if F[m,r+1]==1:
                    F[m,r+1]=choice(P)
                    if F[m,r+1]==2:
                        L.append((m,r+1))
            if V=='SE':#vent du sud est
                if F[m-1,r-1]==1:
                    F[m-1,r-1]=choice(P)
                    if F[m-1,r-1]==2:
                        L.append((m-1,r-1))
                if F[m-1,r]==1:
                    F[m-1,r]=choice(P)
                    if F[m-1,r]==2:
                        L.append((m-1,r))
                if F[m,r-1]==1:
                    F[m,r-1]=choice(P)
                    if F[m,r-1]==2:
                        L.append((m,r-1))
            if V=='NE':#vent du nord est
                if F[m,r-1]==1:
                    F[m,r-1]=choice(P)
                    if F[m,r-1]==2:
                        L.append((m,r-1))
                if F[m+1,r-1]==1:
                    F[m+1,r-1]=choice(P)
                    if F[m+1,r-1]==2:
                        L.append((m+1,r-1))
                if F[m+1,r]==1:
                    F[m+1,r]=choice(P)
                    if F[m+1,r]==2:
                        L.append((m+1,r))
            if V=='NO':#vent du nord ouest
                if F[m+1,r+1]==1:
                    F[m+1,r+1]=choice(P)
                    if F[m+1,r+1]==2:
                        L.append((m+1,r+1))
                if F[m+1,r]==1:
                    F[m+1,r]=choice(P)
                    if F[m+1,r]==2:
                        L.append((m+1,r))
                if F[m,r+1]==1:
                    F[m,r+1]=choice(P)
                    if F[m,r+1]==2:
                        L.append((m,r+1))
            if V=='A':#Absence de vent
                if F[m,r-1]==1:
                    F[m,r-1]=choice(P)
                    if F[m,r-1]==2:
                        L.append((m,r-1))
                if F[m-1,r]==1:
                    F[m-1,r]=choice(P)
                    if F[m-1,r]==2:
                        L.append((m-1,r))
                if F[m+1,r]==1:
                    F[m+1,r]=choice(P)
                    if F[m+1,r]==2:
                        L.append((m+1,r))
                if F[m,r+1]==1:
                    F[m,r+1]=choice(P)
                    if F[m,r+1]==2:
                        L.append((m,r+1))
            F[m,r]=3
            G=F[2:n-2,2:n-2]
            print (G)
            anima.append([matshow(G, fignum=False, animated=True, cmap=cmap)])
            plt.draw() 
            plt.show()
            i=input()
            plt.close()
            if i=='s':
                return ('Fin de la modélisation')
        