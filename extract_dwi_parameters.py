import numpy as np
import pandas as pd
import re
import os

KEY1="##$PVM_DwGradVec="
KEY2="##$PVM_DwEffBval="

'''
Data structure of the target file
##$PVM_DwDir=( 112, 3 )
0.129705582985459 0.172861745083561 0.976368413473658 -0.482657029520601 
0.281067646465789 0.829483676731816 -0.187812786427214 -0.375659578124733 
0.907527541520142 0.514580221281473 -0.309726986323259 0.79954761572343 
0.652087947068601 0.372677764036738 0.660221624517431 0.0414513540615393 
0.735256725113697 0.676520017014683 -0.743955379444463 -0.260941271375216 
0.615174809536876 -0.455570292140411 -0.79494401224997 0.400649131169682
'''
def extract_mat(method_text,key):
    '''
    Extracting data following the {key} until it finds next key by ##
    '''
    subm=method_text[method_text.find(key)+len(key):]
    subm=subm[:subm.find("##")]
    subm=subm.replace(" ","\n").replace("\n\n","\n")
    return subm

def str2array(mat):
    '''
    converting str numbers to numpy array
    '''
    mat=map(lambda x:float(x),filter(lambda x:len(x)>0,mat.split("\n")))
    return np.array(list(mat))


def create_b_table(m_file):
    with open(m_file) as f:
        method_text = f.readlines()
        method_text="\n".join(method_text)

    # extracting b vectors
    param,zmat,mat=extract_mat(method_text,KEY1).split(")")
    mat=str2array(mat)
    pattern = r'@(\d+)\*\(0'
    match = re.search(pattern, zmat)
    int(match.group(1))
    mat=np.concatenate([np.zeros(int(match.group(1))),mat])
    d=pd.DataFrame(mat.reshape([-1,3]),columns=["bx","by","bz"])

    # extracting b values
    param,mat=extract_mat(method_text,KEY2).split(")")
    mat=str2array(mat)
    d["b"]=mat

    d=d[["b","bx","by","bz"]]
    d.to_csv(os.path.join(os.path.dirname(m_file),"b_table.txt"), 
            index = False)

m_file=r"V:\MRI_analysis\minori-DTI\20230814_084507_Yagishita_Sharapova_20230814_hf3_s2_icr_1_18\method"
create_b_table(m_file)
