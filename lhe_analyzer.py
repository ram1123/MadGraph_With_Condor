#!/usr/bin/env python
import sys, math, ROOT, copy
ROOT.gROOT.SetBatch(True)

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit

def lhep_pdgID  (line): return int  (line.split()[ 0])
def lhep_status (line): return int  (line.split()[ 1])
def lhep_mother1(line): return int  (line.split()[ 2])
def lhep_mother2(line): return int  (line.split()[ 3])
def lhep_px     (line): return float(line.split()[ 6])
def lhep_py     (line): return float(line.split()[ 7])
def lhep_pz     (line): return float(line.split()[ 8])
def lhep_E      (line): return float(line.split()[ 9])
def lhep_M      (line): return float(line.split()[10])

def print_lhep(l):
    print lhep_pdgID  (l),
    print lhep_status (l),
    print lhep_mother1(l),
    print lhep_mother2(l),
    print lhep_px     (l),
    print lhep_py     (l),
    print lhep_pz     (l),
    print lhep_E      (l),
    print lhep_M      (l)

    return

### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 2:
        KILL('two command-line arguments required: [1] input .lhe file, [2] output .root file')

    ifile  = file      (sys.argv[1], 'r')
    ofile = ROOT.TFile(sys.argv[2], 'recreate')

    higgsPt = ROOT.TH1F('higgsPt', 'higgsPt', 25, 0, 500)

    ###

    event_num_max = -1

    orig_wgt_label = 'SM'
    Nwgts = 1
    wgt_id = [orig_wgt_label]

    event_num, in_event = 0, False
    for line in ifile:
        if line[:1] == '#': continue
        if line.startswith('<scales'): continue
        if event_num_max > 0:
            if event_num > event_num_max: continue
        if line.startswith('<event>'):
            event_num += 1
            weight = {}
            genp_ls = []
            in_event = True
        if line.startswith('</event>'):
            in_event = False
        if in_event:
            #print line
            l0 = line.strip('\n')
            if len(l0.split()) == 6:
                weight[orig_wgt_label] = float(l0.split()[2])
                continue
            if len(l0.split()) == 13:
                p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                p4 = ROOT.TLorentzVector(lhep_px(l0), lhep_py(l0), lhep_pz(l0), lhep_E(l0))
                if lhep_status(l0) == 1 and abs(lhep_pdgID(l0)) == 25:
                    higgsPt.Fill(p4.Pt())
                    #print "Filled: ",lhep_status(l0),lhep_pdgID(l0)
    higgsPt.Write();
    print "ENtries= ",higgsPt.GetEntries();
    c1 = ROOT.TCanvas("c1")
    higgsPt.Draw()
    c1.SaveAs("higgsPt.png")
    print "event number = ",event_num
