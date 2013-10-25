#! /usr/bin/env python


import os, sys
from glob import glob

DirList=['../files/LHE_shapes_8TeV/ggH_CPS','../files/LHE_shapes_8TeV/qqH_CPS_corrected']

MassList=[250,300,350,400,450,500,550,600,700,800,900,1000]

for Indir in DirList :
 for iMass in MassList :
  InFile=glob(Indir+'/*'+str(iMass)+'*.tar.gz')
  print iMass,InFile 
  if len(InFile) == 1 :
    os.system('tar xzf '+InFile[0]+' pwgevents.lhe')
    os.system('python/lheroot.py pwgevents.lhe '+Indir+'/mH'+str(iMass)+'.root') 
    os.system('rm pwgevents.lhe') 
