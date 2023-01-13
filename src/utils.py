# -*- coding: utf-8 -*-
"""
For: UMR TETIS RESEARCH UNIT
Author: rodrique_kafando
"""
import os
import json
import pandas as pd
import numpy as np
from similarity.normalized_levenshtein import NormalizedLevenshtein




def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def manageDir():
    print('managing output directories...')
    DIRLIST = ["./candidates", "./logs", 
               "./remaining", "./defaultgeocoding", "./disambiguated"]
    # If folder doesn't exist, then create it.
    for dirname in DIRLIST:
        CHECK_FOLDER = os.path.isdir(dirname)
        if not CHECK_FOLDER:
            os.makedirs(dirname)
            print("created folder : ", dirname)
        else:
            pass
            print(dirname, "folder already exists.")


def delStrInStr(string: str, find: str, replace: str) -> str:
    temp = string.rsplit(find)
    return replace.join(temp).strip()

def normalizedLevenshtein(w,l):
    rsl = []
    normalized_levenshtein_ = NormalizedLevenshtein()
    tmpl = []
    for i in l:
        simval = normalized_levenshtein_.similarity(w,i)
        tmpl.append((i,simval))
    print("tmpl similarity value :", tmpl)
    if len(tmpl)>0:
        rs = max(tmpl,key=lambda item:item[1])
        rsl.append(rs)
    return rsl

def simplDicToDf(Final):
    df = pd.DataFrame(Final.items())  
    return df

def dicToDf(Final):
    df = pd.DataFrame(Final.items())  
    columns=['Output_sne', 'lat', 'lng', 'Country_Code', 'Type', 'Population', 'Desamb_Phase']
    df[columns] = pd.DataFrame(df[1].tolist(), index=df.index)
    df_ = df[columns]
    df_['input_sne']= df[0]
    return df_

def keys_with_top_values(my_dict):
    return [key  for (key, value) in my_dict.items() if value == max(my_dict.values())]


def read_record(f):
    with open(f, "r") as read_file:
        tmpCand = json.load(read_file)
        tmpCand = tmpCand[0]
    proc_cand =  {}
    for k in tmpCand:
        proc_cand[k] = {}
        for kx in tmpCand[k]:
            proc_cand[k][kx] = {}
            for ky in tmpCand[k][kx]:
                ky_ = delStrInStr(string=ky, find='.', replace='')
                ky_ = delStrInStr(string=ky, find='the ', replace='') # to be remove if you run over the existing geocoded data, 
                                                                    # this fxn is added on the top of GetSne() fxn
                proc_cand[k][kx][ky_] = tmpCand[k][kx][ky]
    return proc_cand

def checkCompletude(w,listofw):
    normalized_levenshtein_ = NormalizedLevenshtein()
    for w_ in listofw:
        if (w.lower() in w_.lower() or w_.lower() in w.lower())  and normalized_levenshtein_.similarity(w,w_)>0.6:
#             print('hight level of substring')
            return 'ok'
        else:
#             print('low level matching')
            pass

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')
