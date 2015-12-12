#### flow data for government securities. 
### Add
from IPython.core.display import display, display_png, display_svg

import random            as rn
import numpy             as np
import scipy             as sp
import networkx          as nx
import matplotlib.pyplot as plt
import scipy.optimize    as opt
import scipy.stats       as st
import pickle            as pk
import matplotlib.colors as colors
import matplotlib.cm     as cm
import sys
import os
import pandas as pd
from copy import deepcopy

from matplotlib.backends.backend_pdf import PdfPages
def main():

    rootWD='/Users/charlotteszostek/Documents/OldProjects/EconomicsProject/Analysis'
    
    os.chdir(rootWD)
    
    
    #### Load data for Government securities
    ## Total
    test=pd.read_csv('MFI_hold_gov_sec.csv')
    MFI_total=pd.DataFrame(data=test)
    MFI_total.index=MFI_total['date']
    MFI_total=MFI_total.drop(['date'],axis=1)
    
    #### euroarea
    test=pd.read_csv('MFI_ea_hold_gov_sec.csv')
    MFI_ea=pd.DataFrame(data=test)
    MFI_ea.index=MFI_ea['Date']
    MFI_ea=MFI_ea.drop('Date',axis=1)
    #### domestic
    test=pd.read_csv('MFI_dom_hold_gov_sec.csv')
    MFI_dom=pd.DataFrame(data=test)
    MFI_dom.index=MFI_dom['date']
    MFI_dom=MFI_dom.drop(['date'],axis=1)
    
    test=pd.read_csv('total_assets_MFI.csv')
    MFI_assets=pd.DataFrame(data=test)
    MFI_assets.index=MFI_assets['Date']
    MFI_assets=MFI_assets.drop(['Date'],axis=1)
    
    
    
    ### ratio domestic to european
    ratios1=MFI_dom/MFI_ea
    ratios2=MFI_dom/MFI_total
    ratios3=MFI_ea/MFI_total
    
    #GDP
    test=pd.read_csv('gdp.csv')
    GDP=pd.DataFrame(data=test)
    GDP.index=GDP['date']
    GDP=GDP.drop(['date'],axis=1)
    
    
    MFI_dom_tGDP=MFI_dom.ix[GDP.index,MFI_dom.columns[1:]]/GDP[MFI_dom.columns[1:]]
    MFI_ea_tGDP=MFI_ea.ix[GDP.index,MFI_ea.columns[1:]]/GDP[MFI_ea.columns[1:]]
    MFI_total_tGDP=MFI_total.ix[GDP.index,MFI_total.columns[1:]]/GDP[MFI_total.columns[1:]]
    
    
    MFI_dom_tAssets=MFI_dom.ix[MFI_assets.index,MFI_dom.columns[1:]]/MFI_assets[MFI_dom.columns[1:]]
    MFI_ea_tAssets=MFI_ea.ix[MFI_assets.index,MFI_ea.columns[1:]]/MFI_assets[MFI_ea.columns[1:]]
    MFI_total_tAssets=MFI_total.ix[MFI_assets.index,MFI_total.columns[1:]]/MFI_assets[MFI_total.columns[1:]]
    
    
    
    
    
    ##### Network for SL-PIN. Network using 
    ### label things
    os.chdir(rootWD)
    test=pd.read_csv('EBA_SovereignExposure.csv')
    S_nw=pd.DataFrame(data=test)
    S_nw.index=S_nw['Period']
    S_nw=S_nw.drop(['Period'],axis=1)
    
    Bank_level=deepcopy(S_nw)   ### MATURITY IS HERE
    
    #### Get codes 
    test=pd.read_csv('country_codes.csv')
    CC=pd.DataFrame(data=test)
    CC.index=CC['NC_code']
    CC=CC.drop(['NC_code'],axis=1)
    ### 2 manual'corrections' for consistency with the BC
    CC.loc[1,'C_code']='AT'
    CC.loc[30,'C_code']='UK'
    
    
    test=pd.read_csv('bank_codes.csv')
    BC=pd.DataFrame(data=test)
    BC.index=BC['Code']
    BC=BC.drop(['Code'],axis=1)
    #with PdfPages('SL-Timeseries') as pdf:   
    
    S_nw['Bank_country']=S_nw.Bank_code
    replace=[]
    for i in np.array(S_nw.Bank_code):
        replace.append(BC.Country[i])
    S_nw['Bank_country']=replace  
    
    S_nw['Soverign_country']=S_nw.Country
    Bank_level['Soverign_country']=Bank_level.Country  
    
    ### Country level
    replace=[]
    for i in np.array(S_nw.Country):
        replace.append(CC.C_code[i])
    S_nw['Soverign_country']=replace 
    ### We drop any think that is not defines with a code in CC
    S_nw=S_nw.dropna()              ### Data is ready here 
    
    
    ### bank level
    replace=[]
    for i in np.array(Bank_level.Country):
        replace.append(CC.C_code[i])
    Bank_level['Soverign_country']=replace    
    ### We drop any think that is not defines with a code in CC
    Bank_level=Bank_level.dropna()                      ### Data is ready here 
    Country_level=S_nw
    return(Bank_level,Country_level)
    
def simulation(Bank_level , Country_level, m, upto):
    
        if upto is True:
            toGrep=np.arange(0,n+1)[1:]
            ### add itteration to conditions or other multiple condition 
        else:
            toGrep=m
            condition=[Bank_level.Maturity==toGrep]  
          
        Bank_level=Bank_level.ix[Bank_level.Maturity==toGrep]            
        Country_level=Country_level.ix[Country_level.Maturity==toGrep] 
        
        return (Bank_level, Country_level) 
        
        
        
        
        
        
        
        
        
        
        
        
        
                
                    
                            
    