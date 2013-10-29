#! /usr/bin/env python

import os, sys
from glob import glob
import ctypes
from ctypes import c_int,c_double,c_float,cdll,byref


import ROOT
from ROOT import *

Config={ '8TeV' : { 
                    'ggH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/ggH_CPS/'           , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'qqH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/qqH_CPS_corrected/' , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'mH'  : [250,300,350,400,450,500,550,600,700,800,900,1000]
                  } 
       } 

Binning={
           250  : [  80  , 0. , 400. ] ,
           300  : [  80  , 0. , 600. ] ,
           350  : [  80  , 0. , 800. ] ,
           400  : [  80  , 0. ,1000. ] ,
           450  : [  80  , 0. ,1500. ] ,
           500  : [  80  , 0. ,2000. ] ,
           550  : [  80  , 0. ,2000. ] ,
           600  : [  80  , 0. ,2000. ] ,
           700  : [  80  , 0. ,3000. ] ,
           800  : [  80  , 0. ,3000. ] ,
           900  : [  80  , 0. ,3000. ] ,
          1000  : [  80  , 0. ,3000. ]
        }


def mkInt(Energy=['8TeV'],Type=['ggH'],MassList=[250,300,350,400,500,600,700,800,900,1000],fOut='mkInt.root'):

   canvas = TCanvas("cfill","cfill",600,600)
   canvas.Divide(1,2)

   
   fWght = TFile("mkWght.root")
   
   for iEnergy in Energy:
     #MassList = Config[iEnergy]['mH']
     for iType in Type:
       for iMass in MassList :
         nBins = Binning[iMass][0]
         xMin  = Binning[iMass][1]
         xMax  = Binning[iMass][2]

         # load weight
         wName = 'wght_mH'+str(iMass)+'_cpsNew_'+iEnergy+'_'+iType
         wCPS  = fWght.Get(wName)
         
         if iMass >= 400 :
           fInt  = TFile('Interference_weights/h_MWW_rel_NNLO_'+str(iMass)+'.root') 
           hInt  = fInt.Get('h_MWW_rel_NNLO_cen')
           print hInt 

           canvas.cd(1)
           hInt.Draw()
           hInt.Smooth(10)
           wInt = TSpline3(hInt)
           wInt.SetLineColor(kRed) 
           wInt.Draw("same")

         #canvas.WaitPrimitive()

  
         # Powheg
         InDir=Config[iEnergy][iType]['pwgDir']
         iFile=InDir+iType+str(iMass)+'.root'
         f = TFile(iFile)
         t= f.Get("latino/latino")
         nentries = t.GetEntries()
         hName='mH'+str(iMass)+'_powheg_'+iEnergy+'_'+iType
         hPowheg = TH1F(hName,hName,nBins,xMin,xMax)
         hPowheg.Sumw2()
         hName   ='mH'+str(iMass)+'_cps_'+iEnergy+'_'+iType
         hCPS    = TH1F(hName,hName,nBins,xMin,xMax)
         hCPS.Sumw2()
         hName   ='mH'+str(iMass)+'_cpsInt_'+iEnergy+'_'+iType
         hCPSInt = TH1F(hName,hName,nBins,xMin,xMax)
         hCPSInt.Sumw2()
         step = 5000
         for i in xrange(nentries):
           #if i > 0 and i%step == 0: print i,' events processed.' 
           t.GetEntry(i)
           mH = getattr(t,'MHiggs') 
           wghtCPS = wCPS.Eval(mH)
           wghtInt = 1. 
           if mH < 1000. and iMass>=400:
             wghtInt = wInt.Eval(mH) 
           #print mH, wghtCPS, wghtInt
           hPowheg.Fill(mH,1.)
           hCPS   .Fill(mH,wghtCPS)
           hCPSInt.Fill(mH,wghtCPS*wghtInt)


         canvas.cd(2)
         hPowheg.SetLineColor(kBlack)
         hCPS   .SetLineColor(kBlue)
         hCPSInt.SetLineColor(kRed)
         hCPSInt.Draw("hist")
         hCPS   .Draw("histsame")
         hPowheg.Draw("histsame")

         sName= 'mH'+str(iMass)+'_cpsInt_'+iEnergy+'_'+iType 
         canvas.SaveAs('plots/'+sName+'.pdf')
         #canvas.WaitPrimitive()

   fWght.Close()
   

mkInt()
