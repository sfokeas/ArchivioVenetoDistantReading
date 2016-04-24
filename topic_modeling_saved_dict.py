import string
import sys

from gensim import corpora
from gensim.models import ldamodel
from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer
from nltk.tokenize import TreebankWordTokenizer
import  pickle

if len(sys.argv) != 2:
    print "usage: application <number of topics> "
    sys.exit(1)

numTopics = int(float(sys.argv[1]))


# dictionary.save('pureDictionary.dict')
dictionary = corpora.Dictionary.load('filteredDictionary_above_4_below_2.dict')

corpus = pickle.load( open( "corpus.pkl", "rb" ) )

lda = ldamodel.LdaModel(corpus, id2word=dictionary,
                        num_topics=numTopics)  # model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary) # tfidf = models.TfidfModel(corpus); corpus_tfidf = tfidf[corpus]; lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

lda.save('lda_' + 'topics_' + str(numTopics) +'.model')

outputFile = open('topics_' + str(numTopics) + ".topics", 'w')

out = lda.print_topics(numTopics, 40)
for ind in out:
    for ind2 in ind:
        if isinstance(ind2, (int)):
            print >> outputFile, ind2
        else:
            print >> outputFile, ind2.encode('utf8')

outputFile.close()
