import ROOT
ROOT.gROOT.SetBatch(True)

f1 = ROOT.TFile('ppH_1j_SM.root',"READ")
f2 = ROOT.TFile('ppH_1j_SMEFTsim_A_U35_alphaScheme_UFO_v2_1.root',"READ")

h1 = f1.Get("higgsPt")
h1.SetLineColor(1)
h2 = f2.Get("higgsPt")
h2.SetLineColor(2)


c1 = ROOT.TCanvas("c1")
#c1.SetLogy(1)
#h1.Draw("")
#h2.Draw("same")
rp = ROOT.TRatioPlot(h1,h2);
c1.SetTicks(0,1)
rp.Draw()
rp.GetLowerRefGraph().SetMinimum(0)
rp.GetLowerRefGraph().SetMaximum(2)
c1.Update()
c1.SaveAs("overlap.png")
