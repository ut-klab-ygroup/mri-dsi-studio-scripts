import os, shutil,glob
import re
raw_dir=r"V:\MRI_rawdata\Minori project"
prj_dir=r"V:\MRI_analysis\minori-DTI"

target_protocols=["<NODDI_3b_ver2>"]

def copy_file(date_name,prtcl,from_f):
    to_prj=os.path.join(prj_dir,date_name)
    nifti_dir=os.path.join(to_prj,"nifti_"+prtcl.replace("<","").replace(">",""))
    for d in [to_prj,nifti_dir]:
        if not os.path.exists(d):
            os.mkdir(d)
    to_f=os.path.join(nifti_dir,os.path.basename(from_f))
    if not os.path.exists(to_f):
        shutil.copy(from_f,to_f)

for r in glob.glob(os.path.join(raw_dir,"2*")):
    if not os.path.isdir(r):
        continue
    print(r)
    for s in glob.glob(os.path.join(r,"*")):
        if not os.path.isdir(s):
            continue
        if os.path.basename(s)[0]=="A":
            continue

        acqp_f=os.path.join(s,"acqp")
        if not os.path.exists(acqp_f):
            continue

        with open(acqp_f) as f:
            acqp=f.readlines()
            acqp="".join(acqp)
        
        p_idx_s=acqp.find("##$ACQ_protocol_name")
        p_idx_e=acqp.find("##$ACQ_scan_name")
        if p_idx_s<0:
            continue
        param,protocol,_=acqp[p_idx_s:p_idx_e].split("\n")
        if protocol not in target_protocols:
            continue   

        nf_list=glob.glob(os.path.join(s,"pdata","1","nifti","*.nii"))
        
        if len(nf_list)<10: #failed protocol? TODO threshold is arbitrary 
            continue
        
        for nf in glob.glob(os.path.join(s,"pdata","1","nifti","*.nii")):
            pattern = r'(\d+_\d+).nii'    #b val 0 vector
            match = re.search(pattern, nf)
            if len(match.group(1))==len("20230908_160553192"):
                continue
            copy_file(os.path.basename(r),protocol,nf)

            for m in ["method","acqp"]:
                from_f=os.path.join(s,m)
                to_f=os.path.join(prj_dir,os.path.basename(r),m)
                if not os.path.exists(to_f):
                    shutil.copy(from_f,to_f)