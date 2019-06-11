sed -i 's/Ext6/Ext7/g' RunMadGraph_EWK.jdl
sed -i 's/Ext6/Ext7/g' RunMadGraph_EWK.sh
sed -i 's/Ext6/Ext7/g' RunMadGraph_QCD.jdl
sed -i 's/Ext6/Ext7/g' RunMadGraph_QCD.sh
sed -i 's/Ext6/Ext7/g' RunMadGraph_EWKaQCD.jdl
sed -i 's/Ext6/Ext7/g' RunMadGraph_EWKaQCD.sh
sed -i 's/set iseed 29/set iseed 39/g' EWK_cards/*.dat
sed -i 's/set iseed 29/set iseed 39/g' QCD_Cards/*.dat
sed -i 's/set iseed 29/set iseed 39/g' EWKaQCD_cards/*.dat
mkdir condor_logs/Ext7/
mkdir condor_logs/Ext7/EWK_cards
mkdir condor_logs/Ext7/QCD_Cards
mkdir condor_logs/Ext7/EWKaQCD_cards
eosmkdir /eos/uscms/store/user/rasharma/MonteCarlo_Samples/Ext7
eosmkdir /eos/uscms/store/user/rasharma/MonteCarlo_Samples/Ext7/EWK
eosmkdir /eos/uscms/store/user/rasharma/MonteCarlo_Samples/Ext7/QCD
eosmkdir /eos/uscms/store/user/rasharma/MonteCarlo_Samples/Ext7/EWKaQCD
condor_submit RunMadGraph_EWK.jdl
condor_submit RunMadGraph_QCD.jdl
condor_submit RunMadGraph_EWKaQCD.jdl
