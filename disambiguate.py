# -*- coding: utf-8 -*-
"""
For: UMR TETIS RESEARCH UNIT
Author: rodrique_kafando
"""

import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import json
import operator
from math import isclose
from titlecase import titlecase

import utils
import params



utils.manageDir()


def getAmbAndNonAmbigusSne(assne, notassne): #strictly one
    NonAmbigusSne = {}
    AmbigusSne = {}
    AllCcode = {}
    NonAmbCcode = {}
    NoMatch = []
    for sneCandK in assne:
#         sneCandK = delDoteInStr(string=sneCandK, find='.', replace='')
        tuples = [tuple(i) for i in assne[sneCandK]]
#         print("******",(tuples))
        AllCcode[sneCandK] = list(set([x[3] for x in tuples]))
        if len(set(tuples)) ==0:
            NoMatch.append(sneCandK)
            
        elif len(set(tuples)) ==1:
            NonAmbigusSne[sneCandK] = {}
            NonAmbigusSne[sneCandK] = tuples[0]
            NonAmbCcode[sneCandK] = list(set([x[3] for x in tuples]))
            print('$$$$$1 NonAmbCc', NonAmbigusSne)
        elif len(set([x[3] for x in tuples])) == 1:
            for i in tuples:
                if i[4]=='A' and  i[5]==max(tuples,key=lambda item:item[5])[5]:
    #                 print("***",tuples[0])
                    NonAmbigusSne[sneCandK] = {}
                    NonAmbigusSne[sneCandK] =i# tuples[i]
                    NonAmbCcode[sneCandK] = list(set([x[3] for x in tuples]))
                    print('$$$$$2 NonAmbCc', NonAmbigusSne)

                elif i[4]=='P' and i[5]==max(tuples,key=lambda item:item[5])[5]:
    #                 print("$$$",tuples[0])
                    NonAmbigusSne[sneCandK] = {}
                    NonAmbigusSne[sneCandK] = i# tuples[i]  
                    NonAmbCcode[sneCandK] = list(set([x[3] for x in tuples]))
                    print('$$$$$3 NonAmbCc', NonAmbigusSne)                   
        else:
            AmbigusSne[sneCandK] = {}
            AmbigusSne[sneCandK]=tuples
        if len(NoMatch)>0:
            print("No match for SNE in :", list(set(NoMatch)))
            print("\n")
            

    for amb in notassne:        
        tuples_ = [tuple(i) for i in notassne[amb]]            
        if len(notassne[amb])==1:
            NonAmbigusSne[amb] = {}
            NonAmbigusSne[amb] = tuples_[0]
#             NonAmbCcode[sneCandK] = list(set([x[3] for x in tuples]))
            print('NotAsSne but non Ambig :', NonAmbigusSne) 
            notassne = utils.removekey(notassne, amb)

    return NonAmbigusSne, AmbigusSne, AllCcode, NonAmbCcode, notassne


## levensthein similarity measure with, adapted with normalization
## kepping only AMbiguous SNE for evaluation need
def fuzzyMatch(NotAsSne):
    """
    @NotAsSne: Set of sne where candidates names not as the input
    @ desambWithFuzzy: sne desambiguated with fuzzy match conditions
    @toBeDesambAgain: remaining set of sne (should be desambiguate again) using other strategies
    """
    desambWithFuzzy = {}
    toBeDesambAgain = {}
    for amb in NotAsSne:
        print("debugging", amb)
        NotAsSneDesam = {}
        ambL =  list([x[0] for x in NotAsSne[amb]])
        val = utils.normalizedLevenshtein(amb, ambL)
        
        print(amb, val)
        if val is None:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~")
            pass
        elif  len(val)>0:
            MaxSplitVal= max(val[0][0].split(), key=len)
        else:
            print(amb , "has no candidate")
            pass
        
        if len(val)>0 and val[0][1]>=0.8 and amb not in NotAsSneDesam:
#             pc = [x for x in NotAsSne[amb] if x[0]==val[0][0]][0]
            pcs = [x for x in NotAsSne[amb] if x[0]==val[0][0]]#[0]
            pc = max(pcs,key=lambda item:item[5])
#             print('fuzzySWHighMatch1 : ',pc, ' : ', pcx)
            NotAsSneDesam[amb] = pc#.append('fuzzySWHighMatch')
            NotAsSneDesam[amb].append('fuzzySWHighMatch1')
            desambWithFuzzy.update(NotAsSneDesam)
            
        elif utils.checkCompletude(amb,ambL) == 'ok' and amb not in NotAsSneDesam:
#             pc = [x for x in NotAsSne[amb] if x[0]==val[0][0]][0]
            pcs = [x for x in NotAsSne[amb] if x[0]==val[0][0]]#[0]
            pc = max(pcs,key=lambda item:item[5])
            NotAsSneDesam[amb] = pc
            NotAsSneDesam[amb].append('fuzzySWHighMatch2')
            desambWithFuzzy.update(NotAsSneDesam) 
            
        elif len(val)>0 and utils.contains_word(amb, MaxSplitVal) and val[0][1]>=0.3 and amb not in NotAsSneDesam:
#             pc = [x for x in NotAsSne[amb] if x[0]==val[0][0]][0]
            pcs = [x for x in NotAsSne[amb] if x[0]==val[0][0]]#[0]
            pc = max(pcs,key=lambda item:item[5])           
            
            NotAsSneDesam[amb] = pc#.append('fuzzyMWPartialMatch')
            NotAsSneDesam[amb].append('fuzzyMWPartialMatch')
            desambWithFuzzy.update(NotAsSneDesam)
            
        else:
            toBeDesambAgain[amb] = NotAsSne[amb]
            toBeDesambAgain = {k: v for k, v in toBeDesambAgain.items() if k not in desambWithFuzzy}
        print("desambWithFuzzy in loop :", desambWithFuzzy)
    print("End of NotAsSne Desamb :", len(NotAsSne), len(desambWithFuzzy), len(toBeDesambAgain))
    return desambWithFuzzy, toBeDesambAgain

#country_alias

def resolvByAliace(toBeDesambAgain:dict)->dict:
    remainToBeDesambAgain = {}
    resolvedSne = {}
    toBeDesambAgain =  {utils.delStrInStr(string=k, find='.', replace='').lower(): v for k, v in toBeDesambAgain.items()}
    country_alias_ =  {utils.delStrInStr(string=k, find='.', replace='').lower(): v for k, v in params.country_alias.items()}
    for k in toBeDesambAgain:
        if k in country_alias_.keys():
            print('k in alias :', k)
            pc = [v for v in toBeDesambAgain[k] if v[0].lower() in  list(map(lambda x: x.lower(), country_alias_[k]))]
            print("potential candi :", pc)
            if len(pc)>0:
                resolvedSne[k] = pc[0]
                resolvedSne[k].append('resolvedByAliace')
                resolvedSne = {titlecase(k):v for k, v in resolvedSne.items()}
            else:
                remainToBeDesambAgain[k] = toBeDesambAgain[k]
        else:
            remainToBeDesambAgain[k] = toBeDesambAgain[k]
#             resolvedSne[k] = defaultGeocoding_([k], 'en')
#             resolvedSne[k].append('defaultgeo')
            
            
#     resolvedSne = {titlecase(k):v for k, v in resolvedSne.items()}
    remainToBeDesambAgain = {titlecase(k):v for k, v in remainToBeDesambAgain.items()}
    return resolvedSne, remainToBeDesambAgain
        
def scoreWithPop(AmbigusSne, AllCcode, NonAmbCcode):
    Score = {}
    Desambig = {}
    for k in AmbigusSne:
        Score[k] = {}
        for Cc in AllCcode[k]:
            Score[k][Cc] = 0
            for v in AllCcode:
                if Cc in AllCcode[v]:
                     Score[k][Cc] += 1
                else:
                    pass    
                
    for k2 in Score:
        print('%%%%',k2, 'Scoring')
        print({k: v for k, v in sorted(Score[k2].items(), key=lambda item: item[1], reverse=True)})
        bestLoc = None
        potentialLoc = list(utils.keys_with_top_values(Score[k2]))
        print('potentialLoc :', potentialLoc)
        
        if potentialLoc is None:
            print("Their's no potentialLoc for ", k2)
            pass
        
        elif len(potentialLoc) == 1: # when one candidate mutch with the higst score
            bestLoc = potentialLoc[0]
            print('%%%%££££1',bestLoc, 'bestLoc')
            potentialCandid = [c for c in AmbigusSne[k2] if c[3] ==bestLoc]
            print('potentialCandid :', potentialCandid)
            Desambig[k2] = max(potentialCandid,key=lambda item:item[5])
            print("Desambig in Scoring fxn before add 'scoring' :", Desambig)
            Desambig[k2] = list(Desambig[k2])
            Desambig[k2].append('HighPop')
            Desambig[k2] = tuple(Desambig[k2])

        elif len(potentialLoc) > 1: # deal with in case we have equality
            tempLoc = [i for i in  AmbigusSne[k2] if i[3] in potentialLoc]
            bestLoc = max(tempLoc,key=lambda item:item[5])[3]
            print('tempLoc', tempLoc)
            print('%%%%££££2',bestLoc, 'bestLoc')
        
            ######
            potentialCandid = [c for c in AmbigusSne[k2] if c[3] ==bestLoc]
            print('potentialCandid :', potentialCandid)
            Desambig[k2] = max(potentialCandid,key=lambda item:item[5])
            Desambig[k2] = list(Desambig[k2])
            Desambig[k2].append('HighPopInEquality')
            Desambig[k2] = tuple(Desambig[k2])
        else:
            print('this candidate do not match any scoring step : ',k2, AmbigusSne[k2] )
    return Desambig

#### Normal desambguation, without nonAmbiguous SNE in ambiguous (desamb) for evaluation
def Disambiguate( candidates_file, vers : int): # 
    tmpCand = utils.read_record(candidates_file)
    df_list = []
    NonAmblist = []
    Amblist = []
    toBeDesambAgainilist = []
    NonAmbigusSne_list = []
    for k in tmpCand:
        Final = {}
        print('***',k)
        assne = tmpCand[k]['assne']
        notassne = tmpCand[k]['notassne']
    
#         NonAmbigusSne, AmbigusSne, AllCcode, NonAmbCcode = getAmbAndNonAmbigusSne(assne)
        NonAmbigusSne, AmbigusSne, AllCcode, NonAmbCcode, r_notassne  = getAmbAndNonAmbigusSne(assne, notassne)
        
        if len(NonAmbigusSne)>0:
            NonAmbigusSne_df = utils.simplDicToDf(NonAmbigusSne)
            NonAmbigusSne_df['source'] = k
            NonAmbigusSne_list.append(NonAmbigusSne_df)
        else:
            pass
        print('simplDicToDf is done!')
        
        if vers == 'fas':
            print("Input val :", vers)
#             desambWithFuzzy, toBeDesambAgain = fuzzyMatch(notassne)
            desambWithFuzzy, toBeDesambAgain = fuzzyMatch(r_notassne)

            print("desambWithFuzzy : ", desambWithFuzzy)        
            print("toBeDesambAgain", toBeDesambAgain.keys(), '\n')
            print("NonAmbigusSne_list :", NonAmbigusSne)

            if len(desambWithFuzzy)>0:  
                Final.update(desambWithFuzzy)
                print( '###mmmmmmmm',Final)

            else:
                pass
            print('Final update successfully with desambWithFuzzy!')
            
            if len(toBeDesambAgain)>0:
                resolvedSne, remainToBeDesambAgain = resolvByAliace(toBeDesambAgain) # working
                Final.update(resolvedSne)
                print('resolvByAliace is done on :', k)
                df_remainToBeDesambAgain =  utils.simplDicToDf(remainToBeDesambAgain)
                df_remainToBeDesambAgain['source'] = k
                toBeDesambAgainilist.append(df_remainToBeDesambAgain)
            else:
                pass
            print('resolvByAliace is done!') 
            
            if len(AmbigusSne)>0:
                print("********Ambiguous********\n")
                for t in AmbigusSne:
                    print(t , ':', len(AmbigusSne[t]), 'Candidates found')
                print('\n')

                Desambig = scoreWithPop(AmbigusSne, AllCcode, NonAmbCcode)
                print("Desambig :", Desambig)
                Final.update(Desambig)
            else:
                pass
            print('scoreWithPop done!')                 
            
            if len(Final)>0:
                df = utils.dicToDf(Final)
                df['source'] = k
                df_list.append(df)
                print("df_list : ", len(df_list))
            else:
                print('Final dict is empty!')
                pass
            
        ##############################
        elif vers == 'fa':
            desambWithFuzzy, toBeDesambAgain = fuzzyMatch(r_notassne)

            print("desambWithFuzzy : ", desambWithFuzzy)        
            print("toBeDesambAgain", toBeDesambAgain.keys(), '\n')
            print("NonAmbigusSne_list :", NonAmbigusSne)
            

            if len(desambWithFuzzy)>0:  
                Final.update(desambWithFuzzy)
                print( '###mmmmmmmm',Final)

            else:
                pass
            print('Final update successfully with desambWithFuzzy!')
            
 
            if len(toBeDesambAgain)>0:
                resolvedSne, remainToBeDesambAgain = resolvByAliace(toBeDesambAgain) # working
                Final.update(resolvedSne)
                print('resolvByAliace is done on :', k)
                remainToBeDesambAgain.update(AmbigusSne)
                df_remainToBeDesambAgain =  utils.simplDicToDf(remainToBeDesambAgain)
                df_remainToBeDesambAgain['source'] = k
                toBeDesambAgainilist.append(df_remainToBeDesambAgain)
            else:
                pass
            print('resolvByAliace is done!')        

            if len(Final)>0:
                df = utils.dicToDf(Final)
                df['source'] = k
                df_list.append(df)
                print("df_list : ", len(df_list))
            else:
                print('Final dict is empty!')
                pass

        ##############################
        elif vers == 'f':
            desambWithFuzzy, toBeDesambAgain = fuzzyMatch(r_notassne)

            print("desambWithFuzzy : ", desambWithFuzzy)        
            print("toBeDesambAgain", toBeDesambAgain.keys(), '\n')
            print("NonAmbigusSne_list :", NonAmbigusSne)
            
            
            if len(toBeDesambAgain)>0:
                toBeDesambAgain.update(AmbigusSne)
                df_remainToBeDesambAgain =  utils.simplDicToDf(toBeDesambAgain)
                df_remainToBeDesambAgain['source'] = k
                toBeDesambAgainilist.append(df_remainToBeDesambAgain)
            

            if len(desambWithFuzzy)>0:  
                Final.update(desambWithFuzzy)
                print( '###mmmmmmmm',Final)

            else:
                pass
            print('Final update successfully with desambWithFuzzy!')
            

            if len(Final)>0:
                df = utils.dicToDf(Final)
                df['source'] = k
                df_list.append(df)
                print("df_list : ", len(df_list))
            else:
                print('Final dict is empty!')
                pass
           
        else:
            print("Choose valid value ['f' or 'fa' or 'fas'] please")

    if len(NonAmbigusSne_list)>0:
        NonAmbigusSne_final = pd.concat(NonAmbigusSne_list, ignore_index=True)
#         NonAmbigusSne_final.to_csv('../desambiguated/NonAmbigusSne_v'+str(vers)+'.csv')
    else:
        print('NonAmbigusSne df is empty!')
        NonAmbigusSne_final = pd.DataFrame()
        pass
    print('NonAmbigusSne file written with success!')
    
    if len(toBeDesambAgainilist)>0:
        All_toBeDesambAgain = pd.concat(toBeDesambAgainilist, ignore_index=True)
#         All_toBeDesambAgain.to_csv('../remaining/toBeDesambAgain_v'+str(vers)+'.csv')
    else:
        print('toBeDesambAgain df is empty!')
        All_toBeDesambAgain = pd.DataFrame()
#         pass
    print('toBeDesambAgain file written with success!')


    if len(df_list)>0: 
        desambiguated_df =  pd.concat(df_list, ignore_index=True)
    else:
        print('Desambiguated df is empty!')
        desambiguated_df = pd.DataFrame()
#         pass
#     desambiguated_df.to_csv('../desambiguated/'+'desambiguated_v'+str(vers)+'.csv')
    return desambiguated_df, NonAmbigusSne_final , All_toBeDesambAgain
