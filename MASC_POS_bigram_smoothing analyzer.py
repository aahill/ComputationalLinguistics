from nltk.probability import *
from nltk.corpus import CategorizedTaggedCorpusReader
corpus_root = r'C:\Users\Aaron\AppData\Roaming\nltk_data\corpora\masc_tagged' # use your own path
masc = CategorizedTaggedCorpusReader(corpus_root ,'.*/.*',cat_file='categories.txt',sep='_')
cfd1 = ConditionalFreqDist()

for sent in masc.tagged_sents(categories='blog'):
    p = [(None, None)] # empty token/tag pair
    bigrams = zip(p+sent, sent+p)
    for (a,b) in bigrams:
        history = a[1]
        current_tag = b[1]
        #print history, current_tag
        cfd1[current_tag].inc(history)
        
cpd = ConditionalProbDist(cfd1,MLEProbDist)
#turing_cpd = LaplaceProbDist(cpd,len(cfd1.conditions()))
regCpd = ConditionalProbDist(cfd1,MLEProbDist)
laPlaceCpd = ConditionalProbDist(cfd1,LaplaceProbDist)
goodTuringCpd = ConditionalProbDist(cfd1,GoodTuringProbDist)

for a in cfd1:
    for b in cfd1[a]:
            #print b,a, cpd[a]p.rob(b)
            print b,a
            print 'Regular distribution'
            print regCpd[a].prob(b)
            print 'LaPlace smoothing'
            print laPlaceCpd[a].prob(b)
            print 'Turing smoothing'
            print goodTuringCpd[a].prob(b)
            print '---------------------------------'


