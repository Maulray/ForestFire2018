#Influence de la vitesse du vent  
# Hypothèse : la probabilité de propagation suit une fonction du 2nd degré maximale en 70, nulle en 0 et 140, et en dessous(respectivement au delà) de 0 (respectivement (70) 
import numpy as np
from random import*
from matplotlib.pyplot import matshow
import matplotlib.pylab as plt
import matplotlib.animation as animation
from time import*
from matplotlib import *
import math

def f(x):
    ''' prend en argument un x POSITIF et renvoie la probabilité en fonction de la vitesse du vent en km/h'''
    if x>140:
        return 0
    else:
        return math.exp(-0.0015*(x-70)**2)
        
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
    
def liste1(p):
    '''prend en argument une densité d'arbre et renvoie une liste composée de 1 (arbre) et de 0(vide) avec une probabilité p d'apparition du 1'''
    #C'est pour le moment la meilleure piste que j'ai pour intégrer des probabilités
    a=math.floor(100*p)
    L=[]
    for i in range (0,a):
        L.append(1)
    for i in range (0,100-a):
        L.append(0)
    return L
    


#On travaille sur une matrice nxn mais on n'affiche qu'une matrice n-4xn-4 parce que les effets de bord ne sont pas contrôlés   

def crea_foret_feu(n):
    #Création forêt
    cmap1 = colors.ListedColormap(['white','limegreen'])
    cmap2=colors.ListedColormap(['white','limegreen','red'])
    anima=[]
    F=np.zeros((n,n),dtype=int)
    DF=0.8 #probabilité qu'il y ait un arbre sur 1m²
    P=liste1(DF)
    for i in range(0,n):    #Création d'une matrice composée de 1(arbre) et de 0(vide) de façon aléatoire selon la probabilité DF
        for j in range(0,n):
            F[i,j]=choice(P)
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
    
def propag(n,V,K):
    '''Prend en argument un format de matrice carrée, la provenance du vent à choisir parmi 'N', 'S', 'E', 'O', 'NE','NO', 'SO', 'SE', 'A', K la vitesse du vent en km/h et renvoie la création d'une forêt, la mise en feu d'un arbre et la première étape de la propagation'''
    cmap = colors.ListedColormap(['white','limegreen','red','black'])
    anima=[]
    F,L=crea_foret_feu(n)
    input()
    plt.close()
    p=f(K) #On suppose que la probabilité d'enflammement d'un arbre est de 0.8 quand aucun facteur extérieur n'entre en compte
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
            F[m,r]=3 #Arbre en cendres: détruit mais ne permet plus de propager de le feu
            G=F[2:n-2,2:n-2]
            print (G)
            anima.append([matshow(G, fignum=False, animated=True, cmap=cmap)])
            plt.draw() 
            plt.show()
            i=input()
            plt.close()
            if i=='s':
                return ('Fin de la modélisation')
            