import os
import numpy as np
try:
    from initial_condition_functions import *
except:
    print("ERREUR fatal dans les fonctions")


def test_translate():
             
    table1=translate_vtu_file('out.200000.0000.vtu',decimals=3,directory_vtu=os.path.abspath("."))
    table2=translate_vtu_file('out.5000000.0000.vtu',decimals=3,directory_vtu=os.path.abspath("."))
    err_len1=len(table1)-10000
    err_len2=len(table2)-150

    assert (err_len1==0)
    assert (err_len2==0)

def test_writting():
    
    table1=translate_vtu_file('out.200000.0000.vtu',decimals=5,directory_vtu=os.path.abspath("."))
    table2=translate_vtu_file('out.5000000.0000.vtu',decimals=5,directory_vtu=os.path.abspath("."))
    valeur1=np.array([0.02728,0.02708,0.01612])+(0.001/2)
    valeur2=np.array([-0.06567,-0.06550,0])+(0.0025/2)

    assert(((valeur1[0]-(table1[-1,0]))**2+(valeur1[1]-(table1[-1,1]))**2+(valeur1[2]-(table1[-1,2]))**2<(table1[-1,3])**2))
    assert(((valeur2[0]-(table2[-1,0]))**2+(valeur2[1]-(table2[-1,1]))**2+(valeur2[2]-(table2[-1,2]))**2<(table2[-1,3])**2))