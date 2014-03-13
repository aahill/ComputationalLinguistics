from nltk.probability import *
from nltk.corpus import CategorizedTaggedCorpusReader
##loads text to test
test_text_root = r'C:\Users\Aaron\AppData\Roaming\nltk_data\corpora\masc_tagged_test_text'#USE YOUR OWN DIRECTORY
test_text = CategorizedTaggedCorpusReader(test_text_root ,'.*/.*',cat_file='categories.txt',sep='_')
##loads text for author 1 - the correct author
compairison_text1_root = r'C:\Users\Aaron\AppData\Roaming\nltk_data\corpora\masc_tagged_model_text1'#USE YOUR OWN DIRECTORY
text1 = CategorizedTaggedCorpusReader(compairison_text1_root ,'.*/.*',cat_file='categories.txt',sep='_')
##loads text for author 2 - the incorrect author
compairison_text2_root = r'C:\Users\Aaron\AppData\Roaming\nltk_data\corpora\masc_tagged_model_text2'#USE YOUR OWN DIRECTORY
text2 = CategorizedTaggedCorpusReader(compairison_text2_root ,'.*/.*',cat_file='categories.txt',sep='_')


def geometric_mean(nums):
    ''' 
        Return the geometric average of nums
        @param    list    nums    List of nums to avg
        @return   float   Geometric avg of nums 
    '''
    return (reduce(lambda x, y: x*y, nums))**(1.0/len(nums))
 
test_text_fd = FreqDist()
text1_fd = FreqDist()
text2_fd = FreqDist()


for sent in test_text.tagged_sents():
    for word, tag in sent:
        test_text_fd.inc(word)
        
for sent in text1.tagged_sents():
    for word, tag in sent:
        text1_fd.inc(word)
        
for sent in text2.tagged_sents():
    for word, tag in sent:
        text2_fd.inc(word)
        


test1_num_list = []
for word in text1_fd:
    if test_text_fd[word] == 1:
        test1_num_list.append (text1_fd.freq(word))

test2_num_list = []
for word in text2_fd:
    if test_text_fd[word] == 1:
        test2_num_list.append(text2_fd.freq(word))
        
print 'the geometric mean for the first text is: ',geometric_mean(test1_num_list)
print 'the geometric mean for the second text is: ',geometric_mean(test2_num_list) 
