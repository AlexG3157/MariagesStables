import gurobipy as gp
from gurobipy import GRB

import numpy as np

from GaleShapley import pref_etudiants, pref_spe, matrice_de_rangs, paires_instables, GaleShapleyCoteEtudiant, GaleShapleyCoteParcours

env = gp.Env()

## Q11

def max_min_util():

    etu = pref_etudiants()
    spe, cap = pref_spe()

    pos = np.array(matrice_de_rangs(etu))


    n = len(etu)
    m = len(spe)

    model = gp.Model(env=env)

    # Désactiver prints 
    model.setParam('OutputFlag',0)

    x = model.addMVar((n,m), vtype=GRB.BINARY)
    z = model.addVar(name='z', vtype=GRB.INTEGER)
    
    # Un parcours par étudiant
    model.addConstr(x.sum(axis=1) == 1)
    # Capacité
    model.addConstr(x.sum(axis=0) == np.array(cap))
    # z = utilité minimale (rang maximal) 
    model.addConstr((x * pos).sum(axis=1) <= z)

    # Minimizer le rang maximal 
    model.setObjective(z, GRB.MINIMIZE)
 

    model.Params.TimeLimit = 10.0

    model.optimize()

    if model.Status == GRB.INFEASIBLE: 
        
        return -1

    res = [-1] * n    

    for i in range(n):

        for j in range(m):
            if x[i][j].X > 0.9:
                print(f"etu {i} affecte parcours {j}")
                res[i] = j
    
    return res

## Q12

def max_somme_util():

    etu = pref_etudiants()
    spe, cap = pref_spe()

    pos_spe_etu = np.array(matrice_de_rangs(etu))
    pos_etu_spe = np.array(matrice_de_rangs(spe))

    n = len(etu)
    m = len(spe)

    model = gp.Model(env=env)
    model.setParam('OutputFlag',0)

    x = model.addMVar((n,m), vtype=GRB.BINARY)
    
    # Un parcours par étudiant
    model.addConstr(x.sum(axis=1) == 1)
    # Capacité
    model.addConstr(x.sum(axis=0) == np.array(cap))

                       
    model.setObjective((x*pos_spe_etu).sum() + (x.T*pos_etu_spe).sum(), GRB.MINIMIZE)
 

    model.Params.TimeLimit = 10.0

    model.optimize()

    if model.Status == GRB.INFEASIBLE: 
        
        return -1

    res = [-1] * n    

    for i in range(n):

        for j in range(m):
            if x[i][j].X > 0.9:
                print(f"etu {i} affecte parcours {j}")
                res[i] = j
    
    return res

## Q 13
def max_somme_util_k(k : int):

    etu = pref_etudiants()
    spe, cap = pref_spe()

    pos_spe_etu = np.array(matrice_de_rangs(etu))
    pos_etu_spe = np.array(matrice_de_rangs(spe))

    n = len(etu)
    m = len(spe)

    model = gp.Model(env=env)
    model.setParam('OutputFlag',0)

    x = model.addMVar((n,m), vtype=GRB.BINARY)
    
    # Un parcours par étudiant
    model.addConstr(x.sum(axis=1) == 1)
    # Capacité
    model.addConstr(x.sum(axis=0) == np.array(cap))
    # K premiers choix
    model.addConstr((x*pos_spe_etu).sum(axis=1) <= k*np.ones(n))

                       
    model.setObjective((x*pos_spe_etu).sum() + (x.T*pos_etu_spe).sum(), GRB.MINIMIZE)
 

    model.Params.TimeLimit = 10.0

    model.optimize()

    if model.Status == GRB.INFEASIBLE: 
        
        return -1

    res = [-1] * n    

    for i in range(n):

        for j in range(m):
            if x[i][j].X > 0.9:
                print(f"etu {i} affecte parcours {j}")
                res[i] = j
    
    return res

def stats_affectation(aff):

    etu = pref_etudiants()
    spe, cap = pref_spe()

    n = len(etu)
    m = len(spe)

    pos_spe_etu = np.array(matrice_de_rangs(etu))
    pos_etu_spe = np.array(matrice_de_rangs(spe))

    print(f"{len(paires_instables(spe, etu, aff))} paires instables")

    ut_etu = 0
    ut_par = 0

    min_ut_etu = 879132
    min_ut_spe = 879132

    for i in range(n):

        min_ut_etu = min(min_ut_etu, m-pos_spe_etu[i][aff[i]]-1)
        ut_etu += m-pos_spe_etu[i][aff[i]]-1

        min_ut_spe = min(min_ut_spe, n-pos_etu_spe[aff[i]][i]-1)
        ut_par += n-pos_etu_spe[aff[i]][i]-1

    print(f'Somme utilité (parcours et étudiants): {ut_etu+ut_par}')

    print(f'Utilité moyenne étudiant : {ut_etu/n}')
    print(f'Utilité moyenne spe : {ut_par/n}')

    print(f'Utilité minimal étudiant : {min_ut_etu}')
    print(f'Utilité minimale spé : {min_ut_spe}')

def print_stats():
    print("GS cote etudiants")
    stats_affectation(GaleShapleyCoteEtudiant())
    print("GS cote parcours")
    stats_affectation(GaleShapleyCoteEtudiant())
    print("LP max min util")
    stats_affectation(max_min_util())
    print("LP max somme util")
    stats_affectation(max_somme_util())
    print("LP max somme util, k premiers choix")

    for k in range(10):

        print(f"k={k+1}")
        res = max_somme_util_k(k)
        
        if res == -1: print("Unfeasible")
        else: stats_affectation(res)


print_stats()