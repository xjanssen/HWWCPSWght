#! /usr/bin/env python

import os, sys
from glob import glob
import ctypes
from ctypes import c_int,c_double,c_float,cdll,byref


Config={ '8TeV' : { 
                    'ggH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/ggH_CPS/'           , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'qqH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/qqH_CPS_corrected/' , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'mH'  : [250,300,350,400,450,500,550,600,700,800,900,1000]
                  } 
       } 

Binning={
           250  : [  800  , 0. , 400. ] ,
           300  : [  800  , 0. , 600. ] ,
           350  : [  800  , 0. , 800. ] ,
           400  : [  800  , 0. ,1000. ] ,
           450  : [  800  , 0. ,1500. ] ,
           500  : [  800  , 0. ,2000. ] ,
           550  : [  800  , 0. ,2000. ] ,
           600  : [  800  , 0. ,2000. ] ,
           700  : [  800  , 0. ,3000. ] ,
           800  : [  800  , 0. ,3000. ] ,
           900  : [  800  , 0. ,3000. ] ,
          1000  : [  800  , 0. ,3000. ] 
        } 


import ROOT
from ROOT import *



   

def mkHist(Energy=['8TeV'],Type=['ggH','qqH'],MassList=[1000],fOut='mHist.root'):

 
  # Old CPS (Powheg reweigth)
  widths = {
        250  : 4.04e+00,
        300  : 8.43e+00,
        350  : 1.52e+01,
        400  : 2.92e+01,
        450  : 4.69e+01,
        500  : 6.80e+01,
        550  : 9.31e+01,
        600  : 1.23e+02,
        700  : 1.99E+02,
        800  : 3.04E+02,
        900  : 4.49E+02,
        1000 : 6.47E+02,
  }
  scales = {
        'ggH':  {
            250  : 0.949871,
            300  : 0.950109,
            350  : 0.92256,
            400  : 0.863159,
            450  : 0.82215,
            500  : 0.79441,
            550  : 0.772816,
            600  : 0.756956,
            700  : 0.754791,
            800  : 0.775468,
            900  : 0.55175,
            1000 : 0.878601,
        },
        'qqH':  {
            250  : 0.954932,
            300  : 0.962449,
            350  : 0.957838,
            400  : 0.940355,
            450  : 0.948707,
            500  : 0.996891,
            550  : 1.05551,
            600  : 1.12096,
            700  : 1.28318,
            800  : 1.48592,
            900  : 1.13413,
            1000 : 2.0193,
        },
  }
  mt     = c_double(172.5)
  BWflag = c_int(0)
  m      = c_double(0.)
  w      = c_double(1.)
  lib = cdll.LoadLibrary('libMMozerpowhegweight.so')

    

  fOut = TFile(fOut,"RECREATE") 
  canvas = TCanvas("cfill","cfill",600,600)

 

  for iEnergy in Energy:
    MassList = Config[iEnergy]['mH']
    for iType in Type:
      for iMass in MassList :
        nBins = Binning[iMass][0]
        xMin  = Binning[iMass][1]
        xMax  = Binning[iMass][2]

     # New CPS 
        InDir=Config[iEnergy][iType]['cpsDir'] 
        iFile=InDir+'mH'+str(iMass)+'.root'
        f = TFile(iFile)
        t= f.Get("Physics")
        hName='mH'+str(iMass)+'_cpsNew_'+iEnergy+'_'+iType
        print hName
        h = TH1F(hName,hName,nBins,xMin,xMax)
        h.Sumw2()
        t.Draw("M >> %s"%(h.GetName()),"PID==25")
        #canvas.WaitPrimitive()
        # save
        gDirectory.cd('%s:/'%fOut.GetName())
        h.Write(h.GetName(),TH1.kOverwrite)
        # clean
	h.Delete()
        #t.Delete()
        f.Close()

     # Powheg
        InDir=Config[iEnergy][iType]['pwgDir'] 
        iFile=InDir+iType+str(iMass)+'.root'
        f = TFile(iFile)
        t= f.Get("latino/latino")
        hName='mH'+str(iMass)+'_Powheg_'+iEnergy+'_'+iType
        print hName
        h = TH1F(hName,hName,nBins,xMin,xMax)
        h.Sumw2()
        t.Draw("MHiggs >> %s"%(h.GetName()))
        #canvas.WaitPrimitive()
        # save
        gDirectory.cd('%s:/'%fOut.GetName())
        h.Write(h.GetName(),TH1.kOverwrite)
        # clean
	h.Delete()
        #t.Delete()
        f.Close()

  # Old CPS 
        InDir=Config[iEnergy][iType]['pwgDir'] 
        mh = c_double(iMass)
        gh = c_double(widths[iMass])
        iFile=InDir+iType+str(iMass)+'.root'
        f = TFile(iFile)
        t= f.Get("latino/latino")
        nentries = t.GetEntries()
        hName='mH'+str(iMass)+'_cpsOld_'+iEnergy+'_'+iType
        print hName
        h = TH1F(hName,hName,nBins,xMin,xMax)
        h.Sumw2()
        step = 5000
        for i in xrange(nentries):
          #if i > 0 and i%step == 0: print i,' events processed.' 
          t.GetEntry(i)
          m.value  = getattr(t,'MHiggs') 
          #   void pwhg_cphto_reweight_(double *mh, double *gh, double *mt, int *BWflag, double *m, double *w);
          lib.pwhg_cphto_reweight_(byref(mh),byref(gh),byref(mt),byref(BWflag),byref(m),byref(w)) 
          h.Fill(m.value,w.value*scales[iType][iMass])
        #canvas.WaitPrimitive()
        # save
        gDirectory.cd('%s:/'%fOut.GetName())
        h.Write(h.GetName(),TH1.kOverwrite)
        # clean
	h.Delete()
        #t.Delete()
        f.Close()

   


  canvas.Close()
  fOut.Close()


####################################################################################################
if __name__=='__main__':
	mkHist()

