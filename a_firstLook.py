#### flow data for government securities. 
### EDITED ON 12 DEC. 
### DATA MANIPULATION and IMPORT
### BASIC PLOTS FOR INTRODUCTIONS

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
rootWD='/Users/charlotteszostek/Documents/OldProjects/EconomicsProject/CodeANdData/Analysis'

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



if MFI_ea.index[0] is MFI_dom.index[0]:
    print 'fine'
else: 
    print 'start out'
         
if MFI_ea.index[-1] is MFI_dom.index[-1]:
    print 'fine'
else: 
    print 'end out'    

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

### size over time 
if not os.path.exists(rootWD+'/Figures'):
    os.mkdir(rootWD+'/Figures')

fig_path=(rootWD+'/Figures/GovBond_Timeseries')

with PdfPages(fig_path+'Country_Aggregates_GS_all.pdf') as pdf:   
    #convert to millions. 
    MFI_total=MFI_total/1000000
    q=MFI_total.plot(title='Country level aggregate of MFI held government securities')    
    q.set_ylabel('Aggregate of government securities (millions)')
    
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])

    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 

with PdfPages(fig_path+'Ratio_dom_EA_GS.pdf') as pdf:  
    frame=ratios1.loc['31/01/01':,['BE','CY','DE','ES','FR','GR','IE','IT','PT']]
    q=frame.plot(title='Government Securties, Ratio of Domestic to extra European Area')
    
    plt.xticks(rotation=70)   
    q.set_ylabel('Ratio of Domestic to extra EA government securities')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])
    
    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 

with PdfPages(fig_path+'GS_Percentage.pdf') as pdf:     
    frame2=MFI_total.loc['31/01/01':,['BE','CY','DE','ES','FR','GR','IE','IT','PT']]
    
    frame3=deepcopy(frame2)
    for c in frame2.columns:
        frame2[c]=frame2[c]/MFI_total.loc['31/01/01':,'Total EA']
    q=frame2.plot(title='Country level aggregate MFI held government securities as a percentage of collective sum for all EA')    
    plt.xticks(rotation=70) 
    q.set_ylabel('Percentage of total government securities held in EA')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    
    ttl = q.title
    ttl.set_position([.5, 1.05])
    
    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 

with PdfPages(fig_path+'Country_Aggregates_GS_selective.pdf') as pdf:             
    # in millions
    frame3=frame3/1000000
    q=frame3.plot(title='Country level aggregate of MFI held government securities') 
    
    plt.xticks(rotation=70)   
    q.set_ylabel('Aggregate of government securities (millions)')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])

    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 

    
with PdfPages(fig_path+'Domestic_gov_sec_totals.pdf') as pdf:   
    frame=frame/1000000  
    frame=MFI_dom_tGDP.loc['31/12/06':,['BE','CY','DE','ES','FR','GR','IE','IT','PT']]
    q=frame.plot(title='Domestic Government securities held, normalised to GDP')    
  
    plt.xticks(rotation=70)
    q.set_ylabel('Domestic government securities (millions)')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])

    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 


with PdfPages(fig_path+'EA_gov_sec_totals.pdf') as pdf:  
    frame=frame/1000000          
    frame =MFI_ea_tGDP.loc['31/12/06':,['BE','CY','DE','ES','FR','GR','IE','IT','PT']]
    q=frame.plot(title='European area government securities held, normalised to GDP')    
    
    plt.xticks(rotation=70)
    q.set_ylabel('EA Government securities (millions)')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])

    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 


with PdfPages(fig_path+'TOTAL_gov_sec_totals.pdf') as pdf:  
      
    frame =MFI_total_tGDP.loc['31/12/06':,['BE','CY','DE','ES','FR','GR','IE','IT','PT']]
    frame=frame/1000000
    q=frame.plot(title='Total (EA and Domestic) government securities held, normalised to GDP')    
    
    plt.xticks(rotation=70)
    q.set_ylabel('Total government securities (millions)')
    q.set_xlabel('')
    plt.xticks(rotation=70) 
    ttl = q.title
    ttl.set_position([.5, 1.05])

    handles, labels = q.get_legend_handles_labels()
    lgd = q.legend(handles, labels, loc='upper center', frameon=False, fontsize=12, 
                bbox_to_anchor=[1.1, 1.], handlelength=2, handletextpad=1, columnspacing=2, title='Country')
    pdf.savefig(bbox_inches='tight')
    plt.close() 


##### Network for SL-PIN. Network using 
### label things
os.chdir(rootWD)
test=pd.read_csv('EBA_SovereignExposure.csv')
S_nw=pd.DataFrame(data=test)
S_nw.index=S_nw['Period']
S_nw=S_nw.drop(['Period'],axis=1)
#### Get codes 
test=pd.read_csv('country_codes.csv')
CC=pd.DataFrame(data=test)
CC.index=CC['NC_code']
CC=CC.drop(['NC_code'],axis=1)

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
replace=[]
for i in np.array(S_nw.Country):
    replace.append(CC.C_code[i])
S_nw['Soverign_country']=replace  

### Manual change: 
change=S_nw['Soverign_country']
change.ix[change=='GB']='UK'
S_nw['Soverign_country']=change


features=['Soverign_country','Bank_country','AMOUNT'] 
  
network_data=S_nw[features]  
groups=network_data.groupby(['Bank_country','Soverign_country'],as_index=False).sum() 

G=nx.DiGraph()
G.add_nodes_from(groups['Bank_country'])#,bipartite=0)
G.add_nodes_from(groups['Soverign_country'])#],bipartite=1)
for i in groups.index:
    G.add_edge(groups['Soverign_country'][i], groups['Bank_country'][i], {'weight':groups['AMOUNT'][i]} )
from copy import deepcopy
g=deepcopy(G)

from networkx.algorithms import bipartite
B=nx.DiGraph()
B_groups=deepcopy(groups)
rename=deepcopy(groups['Bank_country'])
for i in rename.unique():
    j= 'MFIs_' + i
    rename.ix[rename==i]=j
B_groups['Bank_country']=rename
B.add_nodes_from(B_groups['Bank_country'],bipartite=0)
B.add_nodes_from(B_groups['Soverign_country'],bipartite=1)
for i in B_groups.index:
    B.add_edge(B_groups['Soverign_country'][i], B_groups['Bank_country'][i], {'weight':groups['AMOUNT'][i]} )

#### OLD NETWORK
 ### check order for direction 


### Structure plots

a=G.degree(weight='weight')
import colorsys
def get_rgb_from_hue_spectrum(percent, start_hue, end_hue):
    # spectrum is red (0.0), orange, yellow, green, blue, indigo, violet (0.9)
    hue = percent * (end_hue - start_hue) + start_hue
    lightness = 0.7
    saturation = 0.5
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return r * 255, g * 255, b * 255


nx.set_node_attributes(G, 'degree', a)
color = {}
pc=[]
for n in G.nodes_iter():
    color[n]=get_rgb_from_hue_spectrum(a[n]/a[max(a)], 0.3, 0.0)
    pc.append(a[n]/a[max(a)])
nx.set_node_attributes(G, 'color', color)

plt.clf()
fig = plt.Figure()
fig.set_canvas(plt.gcf().canvas)
pos = nx.spring_layout(g)
nx.draw_networkx_nodes(G, pos, node_size=600,node_color=pc ,cmap=plt.get_cmap('jet'),labels=G.nodes())#,,
nx.draw_networkx_labels(G,pos,font_size=14)
nx.draw_networkx_edges(G, pos, edge_color='b', arrows=True)
nx.draw_networkx_edges(G,pos,font_size=14)

plt.savefig('directed_Network_2.pdf',bbox_inches="tight")

banks , sov = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(banks) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(sov) ) # put nodes from Y at x=2
col= []
for n, d in B.nodes_iter(data=True):
   col.append(d['bipartite'])
   col[col==1]=='b'
   col[col==0]=='g'
   


fig = plt.Figure()
fig.set_canvas(plt.gcf().canvas)
nx.draw_networkx_nodes(B, pos, node_size=200,node_color=col ,cmap=plt.get_cmap('jet'),labels=B.nodes())#,,
nx.draw_networkx_labels(B,pos,font_size=10)
nx.draw_networkx_edges(B, pos, edge_color='b', arrows=True)
os.chdir(fig_path)
plt.savefig('bipartite_Network_1.pdf')

#plt.show()
    
### Algebraic connectivity
### second-smallest eigenvalue of the Laplacian matrix 

L=nx.directed_laplacian_matrix(G)
eigenValues,eigenVectors=np.linalg.eig(L)


idx = eigenValues.argsort()   
eigenValues = eigenValues[idx]
eigenVectors = eigenVectors[:,idx]



sec_min=idx[1]
np.set_printoptions(precision=4)
AC=eigenValues[sec_min]


g_ac = "%0.4f" % AC

dsi=nx.density(G)
g_ac = "%0.4f" % dsi

#### Directed: Edge density
def plotNetworks(G=[],dsi=[],g_ac=[],name=[]):
    posa=nx.spring_layout(G)
    posb=nx.circular_layout(G)
    nx.draw(G,pos=posa,node_size=600,node_color='c',edge_color='0.3')
    nx.draw_networkx_labels(G,posa,font_size=14)
    ff=('Edge density: ' + str(dsi) +'.')
    f=('Algebraic connectivity: ' + str(g_ac) + '.')
    plt.text(0.6,1.1,ff)
    plt.text(0.63,1.05,f) 
    plt.savefig(fig_path+"network_v1"+name+".png")
    plt.close()
    
    nx.draw(G,pos=posb,node_size=500,node_color='c',edge_color='0.3')
    nx.draw_networkx_labels(G,posb,font_size=14)
    ff=('Edge density: ' + str(dsi) +'.')
    f=('Algebraic connectivity: ' + str(g_ac) + '.')
    plt.text(0.6,1.1,ff)
    plt.text(0.63,1.05,f) 
    plt.savefig(fig_path+"network_v2"+ name+".pdf")
    plt.close()

plotNetworks(G=G,dsi=dsi, g_ac=g_ac, name='_directed')


#plotNetworks(G=G3,dsi=dsi3, g_ac=g_ac3, name='_non_dir')

####

