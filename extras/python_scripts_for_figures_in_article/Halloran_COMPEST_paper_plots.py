# -*- coding: utf-8 -*-
"""
Halloran_COMPEST_paper_plots.py

Dr. Landon Halloran, Uni Neuchatel (www.ljsh.ca)
Oct. 2018

https://github.com/lhalloran/COMPEST

Python script used to make Figures 2, 4, 5, 6 & S2 for the article:    
 L.J.S. Halloran, P. Brunner, & D. Hunkeler (2019). “COMPEST, 
 a PEST-COMSOL interface for inverse multiphysics modelling: 
 Development and application to isotopic fractionation of 
 groundwater contaminants.” Computers and Geosciences.

If you find this code useful, we kindly ask you to cite the above 
paper in any published work. 

"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from cycler import cycler
from matplotlib.colors import LogNorm
from matplotlib import cm

#%% FIGURE 2:

p_H=np.zeros((2,2))
p_H[0,0]=1.00782503224  #mass (amu)
p_H[0,1]=2.01410177811
p_H[1,0]=0.999885       #natural occurance
p_H[1,1]=0.000115

p_C=np.zeros((2,2))
R_VPDB=0.0111802 # Vienna Pee Dee Belemnite
p_C[0,0]=12
p_C[0,1]=13.0033548378
p_C[1,0]=1 - R_VPDB/(1+R_VPDB)
p_C[1,1]=R_VPDB/(1+R_VPDB)

p_Cl=np.zeros((2,2))
R_SMOC=0.319766 # Standard Mean Ocean Chloride
p_Cl[0,0]=34.96885268
p_Cl[0,1]=36.96590259
p_Cl[1,0]=1 - R_SMOC/(1+R_SMOC)
p_Cl[1,1]=R_SMOC/(1+R_SMOC)

m_min=96
m_max=2*13+4*37
m_PCE = []
m_TCE = []
m_DCE = []
p_TCE = []
p_PCE = []
p_DCE = []

cutoff=1E-6
sig_PCE=[]
sig_TCE=[]
sig_DCE=[]

n_iso=[0,1]
for i in n_iso:
    for j in n_iso:
        for k in n_iso:
            for l in n_iso:
                for m in n_iso:
                    for n in n_iso:
                        m_now = p_C[0,i] + p_C[0,j] + p_Cl[0,k] + p_Cl[0,l] + p_Cl[0,m] + p_Cl[0,n]
                        m_PCE.append(m_now)
                        m_now = p_C[0,i] + p_C[0,j] + p_H[0,k] + p_Cl[0,l] + p_Cl[0,m] + p_Cl[0,n]
                        m_TCE.append(m_now)
                        m_now = p_C[0,i] + p_C[0,j] + p_H[0,k] + p_H[0,l] + p_Cl[0,m] + p_Cl[0,n]
                        m_DCE.append(m_now)
                        p_nowP = p_C[1,i]*p_C[1,j]*p_Cl[1,k]*p_Cl[1,l]*p_Cl[1,m]*p_Cl[1,n]
                        p_PCE.append(p_nowP)                        
                        p_nowT = p_C[1,i]*p_C[1,j]*p_H[1,k]*p_Cl[1,l]*p_Cl[1,m]*p_Cl[1,n]
                        p_TCE.append(p_nowT)
                        p_nowD = p_C[1,i]*p_C[1,j]*p_H[1,k]*p_H[1,l]*p_Cl[1,m]*p_Cl[1,n]
                        p_DCE.append(p_nowD)
                        if p_nowP>cutoff:
                              sig_PCE.append([i,j,k,l,m,n,p_nowP])
                        if p_nowT>cutoff:
                              sig_TCE.append([i,j,l,m,n,p_nowT])
                        if p_nowD>cutoff:
                              sig_DCE.append([i,j,m,n,p_nowD])

m_bin = []
p_PCE_bin = []
p_PCE_array = np.asarray(p_PCE)
p_TCE_bin = []
p_TCE_array = np.asarray(p_TCE)
p_DCE_bin = []
p_DCE_array = np.asarray(p_DCE)
for i in np.arange(m_min,m_max+1):
      m_bin.append(i)
      indexmask=np.where(np.logical_and(np.asarray(m_PCE)<i+0.5,np.asarray(m_PCE)>i-0.5))
      p_PCE_bin.append(sum(p_PCE_array[indexmask]))
      indexmask=np.where(np.logical_and(np.asarray(m_TCE)<i+0.5,np.asarray(m_TCE)>i-0.5))
      p_TCE_bin.append(sum(p_TCE_array[indexmask]))
      indexmask=np.where(np.logical_and(np.asarray(m_DCE)<i+0.5,np.asarray(m_DCE)>i-0.5))
      p_DCE_bin.append(sum(p_DCE_array[indexmask]))   
fig1 = plt.figure(figsize=(10,4))
plt.bar(m_bin,p_PCE_bin,color=cm.Reds(255))
plt.bar(m_bin,p_TCE_bin,color=cm.Greens(255))
plt.bar(m_bin,p_DCE_bin,color=cm.Blues(255))
plt.xlabel('mass (amu)')
plt.ylabel('proportion')
plt.figtext(0.2, 0.90, "cDCE", fontsize='large', color=cm.Blues(255))
plt.figtext(0.5, 0.90, "TCE", fontsize='large', color=cm.Greens(255))
plt.figtext(0.8, 0.90, "PCE", fontsize='large', color=cm.Reds(255))
#plt.figtext(0.28, 0.50, "$p_{^1H}=0.999885$\n$p_{^2H}=0.000115$\n$p_{^{12}C}=0.9893$\n$p_{^{13}C}=0.0107$\n$p_{^{35}Cl}=0.7576$\n$p_{^{37}Cl}=0.2424$", fontsize='large', color='k')
plt.yscale('log')
plt.ylim([1E-6,1])
plt.show()

filename1= 'Isotopologue_distributions.xlsx'
xlsxin = pd.ExcelFile(filename1)
datain={}
for j in xlsxin.sheet_names:
    datain[j]=xlsxin.parse(j)
PCEmat=np.zeros((3,5))
TCEmat=np.zeros((3,4))
DCEmat=np.zeros((3,3))

sheetname='PCE'
for nC in np.arange(np.shape(PCEmat)[0]):
    for nCl in np.arange(np.shape(PCEmat)[1]):
        C_criteria = datain[sheetname]['n 13C']==nC
        Cl_criteria = datain[sheetname]['n 37Cl']==nCl
        val=datain[sheetname][C_criteria & Cl_criteria]['proportion']
        PCEmat[(nC,nCl)]=float(val)
sheetname='TCE'
for nC in np.arange(np.shape(TCEmat)[0]):
    for nCl in np.arange(np.shape(TCEmat)[1]):
        C_criteria = datain[sheetname]['n 13C']==nC
        Cl_criteria = datain[sheetname]['n 37Cl']==nCl
        val=datain[sheetname][C_criteria & Cl_criteria]['proportion']
        TCEmat[(nC,nCl)]=float(val)
sheetname='DCE'
for nC in np.arange(np.shape(DCEmat)[0]):
    for nCl in np.arange(np.shape(DCEmat)[1]):
        C_criteria = datain[sheetname]['n 13C']==nC
        Cl_criteria = datain[sheetname]['n 37Cl']==nCl
        val=datain[sheetname][C_criteria & Cl_criteria]['proportion']
        DCEmat[(nC,nCl)]=float(val)        
## PLOTS...
# PCE
nCl=4
fig, ax = plt.subplots(figsize=(10,4))
im=ax.imshow(PCEmat, aspect ='equal',norm=LogNorm(vmin=1E-6, vmax=1),cmap='Reds')
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none') 
fig.colorbar(im, orientation='vertical')
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2) # draw gridlines
ax.set_xticks(np.arange(-.5, nCl+1, 1))
ax.set_yticks(np.arange(-.5, 3, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
# Add text labels
x_positions = np.linspace(start=0, stop=nCl+1, num=nCl+1, endpoint=False)
y_positions = np.linspace(start=0, stop=3, num=3, endpoint=False)
for y_index, y in enumerate(y_positions):
    for x_index, x in enumerate(x_positions):
        label = "{:.2E}".format(PCEmat[(y_index, x_index)])
        text_x = x 
        text_y = y 
        ax.text(text_x, text_y, label, color='black', ha='center', va='center', name='Helvetica',weight='bold')
# TCE
nCl=3
fig, ax = plt.subplots(figsize=(10,4))
im=ax.imshow(TCEmat, aspect ='equal',norm=LogNorm(vmin=1E-6, vmax=1),cmap='Greens')
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none') 
fig.colorbar(im, orientation='vertical')
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2) # draw gridlines
ax.set_xticks(np.arange(-.5, nCl+1, 1))
ax.set_yticks(np.arange(-.5, 3, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
# Add text labels
x_positions = np.linspace(start=0, stop=nCl+1, num=nCl+1, endpoint=False)
y_positions = np.linspace(start=0, stop=3, num=3, endpoint=False)
for y_index, y in enumerate(y_positions):
    for x_index, x in enumerate(x_positions):
        label = "{:.2E}".format(TCEmat[(y_index, x_index)])
        text_x = x 
        text_y = y 
        ax.text(text_x, text_y, label, color='black', ha='center', va='center', name='Helvetica',weight='bold')
# DCE
nCl=2
fig, ax = plt.subplots(figsize=(10,4))
im=ax.imshow(DCEmat, aspect ='equal',norm=LogNorm(vmin=1E-6, vmax=1),cmap='Blues')
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none') 
fig.colorbar(im, orientation='vertical')
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2) # draw gridlines
ax.set_xticks(np.arange(-.5, nCl+1, 1))
ax.set_yticks(np.arange(-.5, 3, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
# Add text labels
x_positions = np.linspace(start=0, stop=nCl+1, num=nCl+1, endpoint=False)
y_positions = np.linspace(start=0, stop=3, num=3, endpoint=False)
for y_index, y in enumerate(y_positions):
    for x_index, x in enumerate(x_positions):
        label = "{:.2E}".format(DCEmat[(y_index, x_index)])
        text_x = x 
        text_y = y 
        ax.text(text_x, text_y, label, color='black', ha='center', va='center', name='Helvetica',weight='bold')

#%%  font attributes:
attr1 = {'fontsize':12}
attr2 = {'fontsize':14}

#%% FIGURE 4

### EX002 Sensitivities:
filenamein='EXAMPLE002_Sensitivities.csv'
datain = pd.io.parsers.read_csv(filenamein,header=3)
fig, ax = plt.subplots()

maxsen= np.max(datain['Sensitivity'])
inds= range(np.shape(datain)[0])
for i in inds:
    y = datain['Sensitivity'][i]/maxsen
    b = ax.bar(i, y, color=(.3,.3,.3), edgecolor='k', bottom=0.001)

paramnames = datain['Parameter name'].tolist()
plt.xticks(inds, paramnames,**attr1)
ax.set_yscale('log')

ax.set_xlabel('Parameter',**attr2)
ax.set_ylabel('Relative sensitivity',**attr2)

#%% FIGURE 5:

# data at 0,-0.2 m, and -0.5 m
ex3folder='EXAMPLE003_output/'
ex3filenames=listdir(ex3folder)
Nfiles=9
Ntsteps=5*10+1
Nz=3
ex3data={}
for file in ex3filenames:
    fullpath=ex3folder+file
    dictlabel=file.split('-')[1].split('.')[0]
    datain = pd.read_csv(fullpath,header=7).values
    temp1=np.zeros([Ntsteps,Nz])
    for zz in range(Nz):
        temp1[:,zz]=datain[np.arange(zz*Ntsteps,(zz+1)*Ntsteps),1]
    ex3data[dictlabel]=temp1

tvec=np.arange(0,10.2,0.2)

thekeys=list(ex3data)
thekeys2=[]
thekeys2.append(thekeys[3:9])
thekeys2.append(thekeys[0:3])
thekeysordered = [item for sublist in thekeys2 for item in sublist]

fig,ax=plt.subplots(3,3,figsize=(10, 8),sharex=True)
cy = cycler('color', [(0.7,0.7,0.4), (0.25,0.55,0.55), (0.30,0.00,0.30)])
for spx in range(3):
    for spy in range(3):
        keynow=thekeysordered[spx+3*spy]
        ax[spx,spy].set_prop_cycle(cy)
        l1,l2,l3= ax[spx,spy].plot(tvec,ex3data[keynow])
        thelabel = keynow.replace('_Concentration',' Conc. [mol/m$^3$]').replace('_deltaCl',' $\delta^{37}$Cl').replace('_deltaC',' $\delta^{13}$C')
        if spx==0:
            psn=(0.5,0.85)
        else:
            psn=(0.5,0.1)
        ax[spx,spy].set_title(thelabel,**attr1,position=psn)
        plt.xlim([0,10])
ax[2,1].set_xlabel('time (yr)',**attr1)
fig.subplots_adjust(hspace=0)
fig.subplots_adjust(wspace=0.3)
fig.legend([l1,l2,l3], ['0 m','-0.2 m','-0.5 m'], loc='lower center',ncol=3)
#%% FIGURE 6:

#Plot SV's and Eigenvectors for EXAMPLE003

xl_file = pd.ExcelFile('EXAMPLE003_SVD.xlsx')
SinVal = xl_file.parse(sheetname=0,header=None)
nSV=SinVal.size
nSVused=6
EigenV = xl_file.parse(sheetname=1,header=None)
EigenVtrans = EigenV.transpose() # don't use this


plt.rcParams.update({'font.size': 12}) # SET FONT SIZE FOR ALL
xtickrot=60
namesofparams=['$R_{PCE}$','$R_{TCE}$','$R_{cDCE}$',
'$D_{PCE}$','$D_{TCE}$','$D_{cDCE}$','$A_{C,p}$','$A_{Cl,p}$',
'$A_{C,s}$','$A_{Cl,s}$','$x_0$','$K_{m,PCE}$','$K_{m,TCE}$','$K_{m,cDCE}$']
thecolour1 = (0.7,0.2,0.2)
thecolour2 = (0.4,0.4,0.4)
cy2 = cycler('color', [(1,0.90,0.80), (0.75,0.85,0.65),(0.5,.6,.7),(0.55,0.35,0.45),(0.2,0.4,0.3),(0.15,0.05,.25)])

# EigenValues...
fig, ax = plt.subplots(figsize=(4, 6))

for i in np.arange(nSV):
    y = SinVal[i][0]/SinVal[0][0]
    if i<nSVused:
        thecolour = thecolour1
    else:
        thecolour = thecolour2    
    b = ax.barh(i, y, color=thecolour, edgecolor='k', left=1E-16)
paramnames = np.arange(1,nSV+1,1)
plt.yticks(np.arange(nSV), paramnames,**attr1)
ax.set_xscale('log')
ax.set_axisbelow(True)
ax.grid(axis='x',color='gray', linestyle='dashed')
ax.set_xlabel('Singular Value (Relative)',**attr2)
ax.invert_yaxis()

# identifiability:
EigenVsq=np.square(EigenV)
Iden = EigenVsq[0]
for i in np.arange(1,nSVused):
    Iden=Iden+EigenVsq[i]
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_prop_cycle(cy2)
theinds = np.arange(1,nSV+1)
p=[None]*nSVused
datanow=EigenVsq[0]
p[0]=ax.barh(theinds, datanow, .5,edgecolor='k')
for i in np.arange(1,nSVused):
    p[i] = ax.barh(theinds, EigenVsq[i], .5, edgecolor='k', left=datanow)
    datanow=datanow+EigenVsq[i]
ax.set_yticks(theinds,)
ax.set_yticklabels(namesofparams,rotation=0)
ax.set_xlabel('Identifiability',**attr2)
fig.legend(p,['EV1','EV2','EV3','EV4','EV5','EV6'],loc='right',ncol=1)

# EigenVectors (lin)
EVmax=np.ceil(np.max(np.max(EigenV)))
EVmin=np.floor(np.min(np.min(EigenV)))
fig, ax = plt.subplots(figsize=(10, 6))
for i in np.arange(nSV):
    valuestoplot=2*((EigenV[i]-EVmin)/(EVmax-EVmin)-0.25)
    if i<nSVused:
        thecolour = thecolour1
    else:
        thecolour = thecolour2
    ax.plot(valuestoplot+nSV-1-i,c=thecolour,linewidth=2)
ax.plot()
ax.set_yticks(np.arange(0.5,nSV+1.5,1))
ax.set_yticklabels(['14','13','12','11','10','9','8','7','6','5','4','3','2','1'])
ax.set_ylabel('Eigenvector number',**attr2)
ax.set_xticks(np.arange(0,nSV,1))
ax.set_xticklabels(namesofparams,rotation=xtickrot)
ax.grid(which='major', linestyle='--', linewidth='0.5', color='.7')

#%% FIGURE S2 (Supplementary Info)

#EXAMPLE004 evolution of values and sensitivities by PEST iteration
datain004= pd.io.parsers.read_csv('EXAMPLE004_Sensitivities.csv',header=0)
fig,ax=plt.subplots(3,1,figsize=(6, 8),sharex=True)
ax[0].plot(datain004['Iteration'],datain004['k value'], 'r',linewidth=2)
ax[0].set_ylabel('Estimated K [m/d]')
ax[1].plot(datain004['Iteration'],datain004['Q value'], 'b',linewidth=2)
ax[1].set_ylabel('Estimated Q [W]')
ax[2].plot(datain004['Iteration'],datain004['k sensitivity'], 'r',datain004['Iteration'],datain004['Q sensitivity'], 'b',linewidth=2)
ax[2].set_ylabel('Sensitivities')
ax[2].set_xlabel('Iteration #')