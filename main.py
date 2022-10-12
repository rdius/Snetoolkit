# -*- coding: utf-8 -*-
import sys
"""
For: UMR TETIS RESEARCH UNIT
Author: rodrique_kafando
"""
from disambiguate import Disambiguate as ds

def applyDesamb(candidates_file, version_list =['f','fa','fas']):
    orig_stdout = sys.stdout
    f = open('./logs/logs.txt', 'w')
    sys.stdout = f
    for v in version_list:
        desambiguated_df, NonAmbigusSne, toBeDesambAgain = ds(candidates_file, v)
        desambiguated_df.to_csv('./desambiguated/'+'desambiguated_'+v+'.csv', index = None)
        NonAmbigusSne.to_csv('./desambiguated/NonAmbigusSne_'+v+'.csv', index = None)
        toBeDesambAgain.to_csv('./remaining/toBeDesambAgain_'+v+'.csv', index = None)

    sys.stdout = orig_stdout
    print("logs saved to ./logs")
    f.close()
