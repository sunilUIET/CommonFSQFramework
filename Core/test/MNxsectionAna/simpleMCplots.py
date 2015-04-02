#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

from HistosHelper import getHistos

from CommonFSQFramework.Core.DrawPlots import DrawPlots

import  CommonFSQFramework.Core.Style

from mnDraw import DrawMNPlots 
#from array import array
from optparse import OptionParser

import sys,os
def main():
    CommonFSQFramework.Core.Style.setTDRStyle()


    parser = OptionParser(usage="usage: %prog [options] filename",
                            version="%prog 1.0")

    parser.add_option("-a", "--histo1",   action="store", dest="histo1", type="string", \
                                help="histo1")

    parser.add_option("-b", "--histo2",   action="store", dest="histo2", type="string", \
                                help="histo2")

    parser.add_option("-v", "--variant",   action="store", dest="variant", type="string", \
                                help="choose analysis variant")

    (options, args) = parser.parse_args()


    (options, args) = parser.parse_args()
    if not options.variant:
        print "Provide analysis variant"
        sys.exit()

    if not options.histo1:
        # -a ptHat,QCD_Pt-15to1000_TuneEE3C_Flat_7TeV_herwigpp
        print "Tell me what to do..."
        sys.exit()

    odir = "~/tmp/simpleMC_{}/".format(options.variant)
    os.system("mkdir -p "+odir)

    todo = []
    todo.append( options.histo1.split(",") )
    labelRaw = options.histo1.split(",")[0] 

    if options.histo2:
        todo.append( options.histo2.split(",") )
    

    histofile = "plotsMNxs_{}.root".format(options.variant)

    histos=getHistos(histofile)
    
    toPlot = {}
    cnt =0
    colors = [2,1]
    for t in todo:
        toPlot[t[1]] = histos[t[1]][t[0]]
        toPlot[t[1]].SetMarkerColor(colors[cnt])
        toPlot[t[1]].SetLineColor(colors[cnt])
        cnt+=1


    maxima = []
    for t in toPlot:
        #print t, toPlot[t].GetName()
        maxima.append(toPlot[t].GetMaximum())

    hmax = max(maxima)*1.05
    for t in toPlot:
        toPlot[t].SetMaximum(hmax)

    if len(toPlot) > 1:
        c = ROOT.TCanvas()
        c.Divide(1,2)
        c.cd(1)
        split = 0.2
        margin = 0.005
        ROOT.gPad.SetPad(.005, split+margin, .995, .995)
        c.cd(2)
        ROOT.gPad.SetPad(.005, .005, .995, split)
        c.cd(1)
        ROOT.gPad.SetTopMargin(0.1)
    else:
        c = ROOT.TCanvas()


    DrawMNPlots.banner()
    firstPass = True
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.85)
    legend.SetFillColor(0)
    for h in toPlot.keys():   # not sure if h in toPlot will always give the same order as h in toPlot.keys()
        if firstPass:
            toPlot[h].Draw()
            firstPass = False
        else:
            toPlot[h].Draw("SAME")
        label = "pythia"
        if "herwig" in h: label = "herwig"
        legend.AddEntry(toPlot[h], label, "pel")

    '''
    legend.AddEntry(central, "data", "pel")
    legend.AddEntry(unc, "syst. unc.", "f")
    legend.AddEntry(genHistoHerwig, "herwig", "l")
    legend.AddEntry(genHistoPythia, "pythia", "l")
    '''
    legend.Draw("SAME")    

    if len(toPlot) > 1:
        c.cd(2)

        h1 = toPlot[toPlot.keys()[0]].Clone()
        h2 = toPlot[toPlot.keys()[1]].Clone()
        frame = ROOT.gPad.DrawFrame(h1.GetXaxis().GetXmin(), 0.7, h1.GetXaxis().GetXmax(), 1.3)
        h1.Divide(h2)
        h1.SetLineColor(1)
        h1.SetMarkerColor(1)
        f = ROOT.TF1("f1", "[0]*x+[1]", h1.GetXaxis().GetXmin(), h1.GetXaxis().GetXmax())

        h1.Draw("SAME")
        h1.Fit(f, "", "", 20, h1.GetXaxis().GetXmax())
        f.SetLineColor(1)
        f.Draw("SAME")

        #frame.GetXaxis().SetRangeUser(5,8)

    c.Print(odir+"/simpleMCplot_{}_{}.png".format(labelRaw, options.variant))
    c.Print(odir+"/simpleMCplot_{}_{}.pdf".format(labelRaw, options.variant))







    #central = filter(lambda  finalSet["merged"])

if __name__ == "__main__":
    main()

