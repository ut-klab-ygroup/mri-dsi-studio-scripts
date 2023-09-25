import numpy as np
import pandas as pd
import re
import os

KEY1="##$PVM_DwGradVec="
KEY2="##$PVM_DwEffBval="

def extract_mat(method_text,key):
    subm=method_text[method_text.find(key)+len(key):]
    subm=subm[:subm.find("##")]
    subm=subm.replace(" ","\n").replace("\n\n","\n")
    return subm

def str2array(mat):
    mat=map(lambda x:float(x),filter(lambda x:len(x)>0,mat.split("\n")))
    return np.array(list(mat))


def create_b_table(m_file):
    with open(m_file) as f:
        method_text = f.readlines()
        method_text="\n".join(method_text)

    param,zmat,mat=extract_mat(method_text,KEY1).split(")")
    mat=str2array(mat)
    pattern = r'@(\d+)\*\(0'
    match = re.search(pattern, zmat)
    int(match.group(1))
    mat=np.concatenate([np.zeros(int(match.group(1))),mat])
    d=pd.DataFrame(mat.reshape([-1,3]),columns=["bx","by","bz"])

    param,mat=extract_mat(method_text,KEY2).split(")")
    mat=str2array(mat)
    d["b"]=mat

    d=d[["b","bx","by","bz"]]
    d.to_csv(os.path.join(os.path.dirname(m_file),"b_table.txt"), 
            index = False)

m_file=r"V:\MRI_analysis\minori-DTI\20230814_084507_Yagishita_Sharapova_20230814_hf3_s2_icr_1_18\method"
create_b_table(m_file)
