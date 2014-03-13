import nltk
from nltk.probability import *
from nltk.corpus import CategorizedTaggedCorpusReader
corpus_root = r'C:\Users\Aaron\AppData\Roaming\nltk_data\corpora\masc_tagged' # use your own path
masc = CategorizedTaggedCorpusReader(corpus_root ,'.*/.*',cat_file='categories.txt',sep='_')

def buildSets(training_set,testing_set,category):
    """
    builds the training and testing sets.
    
    Keyword arguments:
    training_set -> an empty list for storing the sentences that go in the training list
    testing_set -> an empty list for storing the sentences that go in the testing list
        
    """
    print 'compiling training and testing sets...'
    #calculates how many sentences are in the masc corpus
    sentence_counter = 0
    for sent in masc.tagged_sents(categories =category):
        sentence_counter += 1
    #compiles training and testing sets based on sentence counter,
    #and calculates the number of sentences that go in each 
    num_training_sents = sentence_counter*.9
    num_testing_sents = sentence_counter*.1
    i = 0
    for sent in masc.tagged_sents():
        if i < num_testing_sents:
            testing_set.append(sent)
            i += 1        
        else:
            training_set.append(sent)

def calcUnigramCfd(wordOrTag,testing_cfd,training_cfd):
    """
    calculates the conditional frequency distributions for unigrams in the training and testing set

    Keyword arguments:
    wordOrTag -> the string 'word' OR 'tag' corresponding to the type info required
    testing_cfd -> the cfd for the testing set
    training_cfd -> the cfd for the training set
    """
    #if wordOrTag is 'tag':
        #training_cfd = nltk.FreqDist(tag for (word, tag) in training_set)
        #testing_cfd = nltk.FreqDist(word for (word, tag) in testing_set)
    for sent in training_set:
        for word, tag in sent:
            if tag is not '.':
                if wordOrTag is 'tag':
                    training_cfd.inc(tag)
                if wordOrTag is 'word':
                    training_cfd.inc(word)
    for sent in testing_set:
        for word, tag in sent:
            if tag is not '.':
                if wordOrTag is 'tag':
                    testing_cfd.inc(tag)
                if wordOrTag is 'word':
                    testing_cfd.inc(word)

def calcBigramCfd(wordOrTag,testing_cfd,training_cfd):
    """
    calculates the conditional frequency distributions for bigrams in the training and testing set

    Keyword arguments:
    wordOrTag -> the string 'word' OR 'tag' corresponding to the type info required
    testing_cfd -> the cfd for the testing set
    training_cfd -> the cfd for the training set
 
    """
    for sent in testing_set:
        p = [(None, None)] # empty token/tag pair
        bigrams = zip(p+sent, sent+p)
        for (a,b) in bigrams:
            history_word = a[0]
            current_word = b[0]
            history_tag = a[1]
            current_tag = b[1]
            if history_tag is not '.' and current_tag is not '.':
                if wordOrTag is 'tag':
                    testing_cfd.inc((history_tag,current_tag))
                if wordOrTag is 'word':
                    testing_cfd.inc((history_word,current_word))
    for sent in training_set:
        p = [(None, None)] # empty token/tag pair
        bigrams = zip(p+sent, sent+p)
        for (a,b) in bigrams:
            history_word = a[0]
            current_word = b[0]
            history_tag = a[1]
            current_tag = b[1]
            if history_tag is not '.' and current_tag is not '.':
                if wordOrTag is 'tag':
                    training_cfd.inc((history_tag,current_tag))
                if wordOrTag is 'word':
                    training_cfd.inc((history_word,current_word))
                    
def calcTrigramCfd(wordOrTag,testing_cfd,training_cfd):
    """
    calculates the conditional frequency distributions for trigrams in the training and testing set

    Keyword arguments:
    wordOrTag -> the string 'word' OR 'tag' corresponding to the type info required
    testing_cfd -> the cfd for the testing set
    training_cfd -> the cfd for the training set
    
    """ 
    for sent in testing_set:
        p = [(None, None)] # empty token/tag pair
        trigrams = zip(p+p+sent, p+sent+p, sent+p+p)
        for (a,b,c) in trigrams:
            history1 = a[1]
            word_history1 = a[0]
            history2 = b[1]
            word_history2 = b[0]
            current_word = c[0]
            current_tag = c[1]
            if history1 is not '.' and current_tag is not '.' and history2 is not '.':
                if wordOrTag is 'tag':
                    testing_cfd.inc((history1,history2,current_tag))
                if wordOrTag is 'word':
                    testing_cfd.inc((word_history1,word_history2,current_word))
    for sent in training_set:
        p = [(None, None)] # empty token/tag pair
        trigrams = zip(p+p+sent, p+sent+p, sent+p+p)
        for (a,b,c) in trigrams:
            history1 = a[1]
            word_history1 = a[0]
            history2 = b[1]
            word_history2 = b[0]
            current_word = c[0]
            current_tag = c[1]
            if history1 is not '.' and current_tag is not '.' and history2 is not '.':
                if wordOrTag is 'tag':
                    training_cfd.inc((history1,history2,current_tag))
                if wordOrTag is 'word':
                    training_cfd.inc((word_history1,word_history2,current_word))
                
                                
def calcFreqs(ngramType,testing_fd,training_fd):
    """
    calculates the frequencies for the given cfd's in both the training set, and prints the required results

    Keyword arguments:
    ngramType -> a string for the ngram being examined
    training_fd -> a FreqDist for the training set
    testing_fd -> a FreqDist for the testing set
    
    """
    items_not_in_testing_set = 0.0
    items_not_in_training_set = 0.0
    print 'the number of ',ngramType, 'in the testing set is: ',testing_fd.B()      
    print 'the number of ',ngramType, 'in the training set is: ',training_fd.B()            
    #calculates and prints the # of items in the training set but not in the testing set
    for a in training_fd:
        if a not in testing_fd:
            items_not_in_testing_set += 1
    #prints the frequency of the types in the training set that were not observed in the testing set,
    print 'the number of ',ngramType, 'in the training set that were not observed in the testing set is: ',items_not_in_testing_set
    print 100 * (testing_fd.N()/(items_not_in_testing_set + testing_fd.N())), ' % of ',ngramType,' are in the testing set.'
    #calculates and prints the # of items in the testing set but not the training set
    for a in testing_fd:
        if a not in training_fd:
            items_not_in_training_set += 1
            #prints the frequency of the types in the testing set that were not observed in the training set,
    print 'the number of ',ngramType, 'in the testing set that were not observed in the training set is: ',items_not_in_training_set
    print 100 * (training_fd.N()/ (items_not_in_training_set + training_fd.N())), ' % of all observed ',ngramType,' are in the training set.'
    print '-------------------------------------------------------------------------------------------------------'
 
    
            
            
        
#FIELDS---------------------------------------------------
category = 'blog'
##LISTS
training_set = []
testing_set = []
##UNIGRAM CFDs
testing_tag_unigram_cfd = FreqDist()
training_tag_unigram_cfd = FreqDist()
testing_word_unigram_cfd = FreqDist()
training_word_unigram_cfd = FreqDist()
##BIGRAM CFDs
testing_tag_bigram_cfd = FreqDist()
training_tag_bigram_cfd = FreqDist()
testing_word_bigram_cfd = FreqDist()
training_word_bigram_cfd = FreqDist()
##TRIGRAM CFDs
testing_tag_trigram_cfd = FreqDist()
training_tag_trigram_cfd = FreqDist()
testing_word_trigram_cfd = FreqDist()
training_word_trigram_cfd = FreqDist()
#METHOD CALLS----------------------------------------------
buildSets(training_set,testing_set,category)
print 'there are ',len(training_set),' sentences in the training set'
print 'there are ',len(testing_set),' sentences in the testing set'
print '----------------------------------------------------'
##

#unigram tags
calcUnigramCfd('tag',testing_tag_unigram_cfd,training_tag_unigram_cfd)
calcFreqs('tag unigrams',testing_tag_unigram_cfd,training_tag_unigram_cfd)
#unigram words
calcUnigramCfd('word',testing_word_unigram_cfd,training_word_unigram_cfd)
calcFreqs('word unigrams',testing_word_unigram_cfd,training_word_unigram_cfd)
#bigram tags
calcBigramCfd('tag',testing_tag_bigram_cfd,training_tag_bigram_cfd)
calcFreqs('tag bigrams',testing_tag_bigram_cfd,training_tag_bigram_cfd)
#bigram words
calcBigramCfd('word',testing_word_bigram_cfd,training_word_bigram_cfd)
calcFreqs('word bigrams',testing_word_bigram_cfd,training_word_bigram_cfd)
#trigram tags
calcTrigramCfd('tag',testing_tag_trigram_cfd,training_tag_trigram_cfd)
calcFreqs('tag trigrams',testing_tag_trigram_cfd,training_tag_trigram_cfd)
#trigram words
calcTrigramCfd('word',testing_word_trigram_cfd,training_word_trigram_cfd)
calcFreqs('word trigrams',testing_word_trigram_cfd,training_word_trigram_cfd)

