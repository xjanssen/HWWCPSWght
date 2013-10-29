#! /usr/bin/env python

import os, sys
from glob import glob
import ctypes
from ctypes import c_int,c_double,c_float,cdll,byref


import ROOT
from ROOT import *
#from ROOT import RooFit

Config={ '8TeV' : { 
                    'ggH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/ggH_CPS/'           , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'qqH' : { 'cpsDir' : '../files/LHE_shapes_8TeV/qqH_CPS_corrected/' , 'pwgDir' : '../files/Original_shapes_8TeV/' } ,
                    'mH'  : [250,300,350,400,450,500,550,600,700,800,900,1000]
                  } 
       } 


def mkWght(Energy=['8TeV'],Type=['ggH','qqH'],MassList=[250,300,350,400,450,500,550,600,700,800,900,1000],fOut='mkWght.root'):

    fOut = TFile(fOut,"RECREATE")
    fHist =  TFile("mHist.root")  
    canvas = TCanvas("cfill","cfill",600,600)
    canvas.Divide(1,2)


    for iEnergy in Energy:
      for iType in Type:
        for iMass in MassList :

          hcpsOld = fHist.Get('mH'+str(iMass)+'_cpsOld_'+iEnergy+'_'+iType)
          hcpsNew = fHist.Get('mH'+str(iMass)+'_cpsNew_'+iEnergy+'_'+iType) 
          hPowheg = fHist.Get('mH'+str(iMass)+'_Powheg_'+iEnergy+'_'+iType)

          hcpsOld.SetLineColor(kBlue)
          hcpsNew.SetLineColor(kRed)
          hPowheg.SetLineColor(kBlack)

          hcpsOld.Rebin(10)
          hcpsNew.Rebin(10)
          hPowheg.Rebin(10)

          hcpsOld.Scale(1./hcpsOld.Integral());
          hcpsNew.Scale(1./hcpsNew.Integral());
          hPowheg.Scale(1./hPowheg.Integral());


          #hcpsOld.Smooth(10)
          #hcpsNew.Smooth(10)
          #hPowheg.Smooth(10)

          rcpsNew = hcpsNew.Clone("rcpsNew")
          rcpsOld = hcpsOld.Clone("rcpsOld")
          rcpsNew.Divide(hPowheg)
          rcpsOld.Divide(hPowheg)

          canvas.cd(1)
          hcpsOld.Draw()
          hcpsNew.Draw("same")
          hPowheg.Draw("same")

          canvas.cd(2)
          #rcpsOld.GetYaxis().SetRangeUser(0,10.)
          #rcpsOld.Draw("hist")
          #rcpsNew.Draw("hist")
          #rcpsNew.Draw("histsame")
   
          rcpsOldS = rcpsOld.Clone("rcpsOldS")
          rcpsOldS.Smooth(10,"r")
          rcpsOldS.Draw("hist")

          sName   = 'wght_mH'+str(iMass)+'_cpsOld_'+iEnergy+'_'+iType
          print sName
          wO = TSpline3(rcpsOldS) 
          wO.SetName(sName)
          wO.SetTitle(sName)
          wO.SetLineColor(kBlue)
          wO.Draw("same")

          gDirectory.cd('%s:/'%fOut.GetName())
          wO.Write(wO.GetName(),TH1.kOverwrite)


          rcpsNewS = rcpsNew.Clone("rcpsNewS")
          rcpsNewS.Smooth(10,"r")
          rcpsNewS.Draw("histsame")
         
          sName   = 'wght_mH'+str(iMass)+'_cpsNew_'+iEnergy+'_'+iType
          print sName
          wN = TSpline3(rcpsNewS) 
          wN.SetName(sName)
          wN.SetTitle(sName)
          wN.SetLineColor(kRed)
          wN.Draw("same")

          gDirectory.cd('%s:/'%fOut.GetName())
          wN.Write(wN.GetName(),TH1.kOverwrite)

          canvas.SaveAs('plots/'+sName+'.pdf')
          #canvas.WaitPrimitive()

    fOut.Close()

#          # roofit
#          xMin = hcpsOld.GetXaxis().GetXmin()
#          xMax = hcpsOld.GetXaxis().GetXmax()
#          print xMin,xMax
#          m = RooRealVar("m","m",xMin,xMax);
#
#          dPowheg = RooDataHist("Powheg","Powheg",RooArgList(m),hPowheg) 
#          dcpsNew = RooDataHist("Powheg","Powheg",RooArgList(m),hcpsNew) 
#
#          p0_Powheg = RooRealVar("p0_Powheg","p0_Powheg",0.1,0.,1.)
#          p1_Powheg = RooRealVar("p1_Powheg","p1_Powheg",0.1,0.,1.)
#          p2_Powheg = RooRealVar("p2_Powheg","p2_Powheg",0.1,0.,1.)
#          p3_Powheg = RooRealVar("p3_Powheg","p3_Powheg",0.1,0.,1.)
#          p4_Powheg = RooRealVar("p4_Powheg","p4_Powheg",0.1,0.,1.)
#          p5_Powheg = RooRealVar("p5_Powheg","p5_Powheg",0.1,0.,1.)
#          m_Powheg  = RooRealVar("m_Powheg","m_Powheg",float(iMass),0.,1500.)
#          s_Powheg  = RooRealVar("s_Powheg","s_Powheg",float(iMass),0.,1500.)
#          a_Powheg  = RooRealVar("a_Powheg","a_Powheg",-1,-10,10)
#          n_Powheg  = RooRealVar("n_Powheg","n_Powheg",1,0,10)
#          f_Powheg  = RooRealVar("f_Powheg","f_Powheg",.5,0.,1.)
#          mg_Powheg = RooRealVar("mg_Powheg","mg_Powheg",100.,0,1500.)
#          sg_Powheg = RooRealVar("sg_Powheg","sg_Powheg",100.,0,1500.)
#          m2_Powheg  = RooRealVar("m2_Powheg","m2_Powheg",float(iMass),0.,1500.)
#          s2_Powheg  = RooRealVar("s2_Powheg","s2_Powheg",float(iMass),0.,1500.)
#          a2_Powheg  = RooRealVar("a2_Powheg","a2_Powheg",-1,-10,10)
#          n2_Powheg  = RooRealVar("n2_Powheg","n2_Powheg",1,0,10)
#
#
#          ga_Powheg   = RooGaussian("ga_Powheg","ga_Powheg",m,mg_Powheg,sg_Powheg) 
#          brn5_Powheg = RooBernstein("brn5_Powheg","brn5_Powheg",m,RooArgList(p0_Powheg,p1_Powheg,p2_Powheg,p3_Powheg,p4_Powheg,p5_Powheg))
#          cb_Powheg   = RooCBShape("cb_Powheg","cb_Powheg",m,m_Powheg,s_Powheg,a_Powheg,n_Powheg)
#          cb2_Powheg   = RooCBShape("cb2_Powheg","cb2_Powheg",m,m2_Powheg,s2_Powheg,a2_Powheg,n2_Powheg)
#          #mod_Powheg  = RooAddPdf("mod_Powheg","mod_Powheg",RooArgList(cb_Powheg,brn5_Powheg),RooArgList(f_Powheg))
#          #mod_Powheg  = RooAddPdf("mod_Powheg","mod_Powheg",RooArgList(cb_Powheg,ga_Powheg),RooArgList(f_Powheg))
#          mod_Powheg  = RooAddPdf("mod_Powheg","mod_Powheg",RooArgList(cb_Powheg,cb2_Powheg),RooArgList(f_Powheg))
#
#          fit_Powheg = mod_Powheg.fitTo(dPowheg,RooFit.Save())
#          fit_Powheg.Print() 
#          
#
#          canvas = TCanvas("cfit","cfit",600,600)
#          frame = m.frame()
#          dPowheg.plotOn(frame)
#          mod_Powheg.plotOn(frame)
#          canvas.cd()
#          frame.Draw()
#          canvas.WaitPrimitive()
 

               
####################################################################################################
if __name__=='__main__':


    mkWght()
 
