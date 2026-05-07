from collections import deque
import heapq
import numpy as np
import time
import pandas as pd

## TME 1

def pref_etudiants():
    res = []
    with open("PrefEtu.txt", 'r', encoding='utf-8-sig') as f:
        s = f.readline().strip()
        n = int(s)

        for _ in range(n):

            s = f.readline().split()[2:]
            res.append(list(map(int, s)))

    return res

def pref_spe():
    res = []
    with open("PrefSpe.txt", 'r', encoding='utf-8-sig') as f:
        int(f.readline().split()[1])
        n = 10
        cap = list(map(int, f.readline().split()[1:]))

        for _ in range(n):

            s = f.readline().split()[2:]
            res.append(list(map(int, s)))

    return res, cap

def matrice_de_rangs(M):
    """
    Transforme la matrice des préférences en une matrice des rangs.
    """

    res = [[0]*len(M[0]) for _ in range(len(M))]

    for i in range(len(M)):
        for j in range(len(M[0])):
            res[i][M[i][j]] = j
    
    return res


def GaleShapleyCoteParcours(etu = None, spe = None, cap = None, iterations = False):

    if etu == None:
        etu = pref_etudiants()
        spe, cap = pref_spe()

    q = deque([s for s in range(len(spe)) for _ in range(cap[s]) ])

    procahin_etu = [0]*len(spe)

    pos = matrice_de_rangs(etu)
    
    affectations = [(1e8,-1) for _ in range(len(etu))]
    res = [-1]*len(etu)

    it = 0
    while q:

        s = q.pop()
        while True:
            it += 1

            etu_prop = spe[s][procahin_etu[s]]
            procahin_etu[s] += 1

            if affectations[etu_prop][1] != -1:

                priorite, a_remplacer = affectations[etu_prop]

                if pos[etu_prop][s] < priorite:

                    affectations[etu_prop] = (pos[etu_prop][s], s)
                    res[etu_prop] = s
                    q.append(a_remplacer)
                    break
            else:
                affectations[etu_prop] = (pos[etu_prop][s], s)
                res[etu_prop] = s
                break
    
    if iterations : return res, it
    return res

def GaleShapleyCoteEtudiant(etu = None, spe = None, cap = None, iterations = False):

    if etu == None:

        etu = pref_etudiants()
        spe, cap = pref_spe()

    q = deque(range(len(etu)))

    procahin_spe = [0]*len(etu)

    pos = matrice_de_rangs(spe)
    
    affectations = [[]for _ in range(len(spe))]

    res = [-1]*len(etu)
    it = 0

    while q:

        e = q.pop()
        while True:
            it +=1
            spe_prop = etu[e][procahin_spe[e]]
            procahin_spe[e] += 1

            if len(affectations[spe_prop]) >= cap[spe_prop]:

                priorite, a_remplacer = affectations[spe_prop][0]
                if pos[spe_prop][e] < abs(priorite):

                    heapq.heapreplace(affectations[spe_prop],(-pos[spe_prop][e],e))
                    q.append(a_remplacer)
                    res[e] = spe_prop
                    break
            else:
                heapq.heappush(affectations[spe_prop],(-pos[spe_prop][e],e))
                res[e] = spe_prop
                break
    
    if iterations: return res, it
    return res

def paires_instables(spe, etu, affectations_etu):

    n  = len(etu)
    m = len(spe)

    ## Préférences 
    etu_dans_spe = [list(np.argsort(spe[j])) for j in range(m)]
    spe_dans_etu = [list(np.argsort(etu[i])) for i in range(n)]


    ## Affectations

    pires_priorites = [-1 for _ in range(m)]

    for i in range(n):
        
        j = affectations_etu[i]

        if etu_dans_spe[j][i] > pires_priorites[j]:
            pires_priorites[j] = etu_dans_spe[j][i]

    res = set()

    for i in range(n):

        prog = affectations_etu[i]
        classement = spe_dans_etu[i][prog]

        ## On ne regarde que les masters qui sont mieux classés. 
        for k in range(classement):
            
            j = etu[i][k] ## Suivant dans le classement

            if etu_dans_spe[j][i] < pires_priorites[j]:
                res.add((i,j))
    return res


## TME 2

def random_etu(n):
    
    res = []
    
    for _ in range(n):
        
        pref = np.arange(n)
        np.random.shuffle(pref)
        res.append(list(pref))

    return res

def random_spe(n):
    
    res = []
    
    for _ in range(n):
        
        pref = np.arange(n)
        np.random.shuffle(pref)
        res.append(list(pref))

    return res

def pire_cas_etu(n):
    return [list(range(n)) for _ in range(n)]

def pire_cas_spe(n):
    return [list(range(n))[::-1] for _ in range(n)]

def mesurer_temps(start, stop , step, cote_etu = True, pire_cas = False):

    temps = []
    iterations = []

    for n in range(start, stop, step):
        
        cap = [1]*n

        temps_n = []
        iterations_n = []

        for _ in range(10):

            if pire_cas:
                etu = pire_cas_etu(n)
                spe = pire_cas_spe(n)
            else:
                etu = random_etu(n)
                spe = random_spe(n)
            start_t = time.time()
            if cote_etu:
                s, it = GaleShapleyCoteEtudiant(etu, spe, cap, iterations=True)
            else:
                s, it = GaleShapleyCoteParcours(etu,spe,cap,iterations=True)

            end_t = time.time()

            temps_n.append(end_t-start_t)
            iterations_n.append(it)

        temps.append(temps_n)
        iterations.append(iterations_n)

    t_df = pd.DataFrame(temps, index=list(range(start, stop, step)))

    it_df = pd.DataFrame(iterations, index=list(range(start, stop, step)))
    return t_df, it_df







    


    




