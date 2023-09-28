import numpy as np
import pandas as pd
import re
import os,glob

KEY1="##$PVM_DwGradVec="
KEY2="##$PVM_DwEffBval="

'''
Data structure of the target file

##$PVM_DwGradVec=( 117, 3 )
@15*(0) 0.064521938211751 0.0859899364293929 0.485693684080778 
-0.240097352167846 0.139816875273757 0.412625989613309 -0.0934273199526963 
-0.186871555799828 0.451448847548755 0.255977518301849 -0.154073440896538 
0.397734320078137 0.324380626191739 0.185388254773641 0.328426717514166 
0.0206199428273792 0.365752868115775 0.336534339788038 -0.37008000673492 
-0.129805026129484 0.30601821553675 -0.226623076385912 -0.395444261223082 

##$PVM_DwEffBval=( 117 )
26.2853418546134 26.2853418546134 26.2853418546134 26.2853418546134 
26.2853418546134 2002.21714070625 2001.88424136636 2002.06111986066 
2001.81639432404 2001.50062611333 2009.82733614018 2001.39853208161 
2000.91233141637 2001.31477703711 2002.45291036884 2000.54875537212 
2000.89299534972 2000.63094398095 2009.11608560928 2016.09167106058 
2000.51653512506 4006.91702555742 4002.90777736512 4002.98438977906 
4002.63301660557 4002.89923002291 4011.59611102576 4002.36730414986 
4002.20706881931 4004.8212191946 4011.01972732255 4002.10389536859 
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


def create_b_table(m_file,out_file):
    with open(m_file) as f:
        method_text = f.readlines()
        method_text="\n".join(method_text)

    # extracting b vectors
    param,zmat,mat=extract_mat(method_text,KEY1).split(")")
    mat=str2array(mat)
    pattern = r'@(\d+)\*\(0'    #b val 0 vector
    match = re.search(pattern, zmat)
    int(match.group(1))
    mat=np.concatenate([np.zeros(int(match.group(1))),mat])
    d=pd.DataFrame(mat.reshape([-1,3]),columns=["bx","by","bz"])

    # extracting b values
    param,mat=extract_mat(method_text,KEY2).split(")")
    mat=str2array(mat)
    d["b"]=mat

    d=d[["b","bx","by","bz"]]
    d.to_csv(out_file, 
            index = False)



prj_dir=r"V:\MRI_analysis\minori-DTI"
for m in glob.glob(os.path.join(prj_dir,"2*")):
    print(m)
    m_file=os.path.join(m,"method")
    out_file=os.path.join(m,"b_table.txt")
    if not os.path.exists(m_file):
        print("method file does not exist")
        continue
    if os.path.exists(out_file):
        print("Already processed")
        continue
    create_b_table(m_file,out_file)