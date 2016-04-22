import string
import sys

from gensim import corpora
from gensim.models import ldamodel
from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer
from nltk.tokenize import TreebankWordTokenizer

if len(sys.argv) != 6:
    print "usage: application <input filename> <number of topics> <no_above> <no_below> <results Dir>"
    sys.exit(1)

inputFilename = sys.argv[1]
resultsDir = sys.argv[5]
excludeSet = string.punctuation + "0123456789"

numTopics = int(float(sys.argv[2]))
no_above = int(float(sys.argv[3]))
no_below = int(float(sys.argv[4]))

stemmer = ItalianStemmer()
lineCounter = 0


def preprocessLine(strLine):
    global lineCounter
    lineCounter = lineCounter + 1
    print lineCounter
    strLine = strLine.decode('utf8').lower()  # do we really need this? #also add
    strLine = ''.join(
        ch for ch in strLine if ch not in set(excludeSet))  # todo put a print just to now the progress of the algo
    return strLine


print "Start"
# Build dictionary
stopWords = set(stopwords.words('italian'))
tokenizer = TreebankWordTokenizer()

texts = [tokenizer.tokenize(preprocessLine(line)) for line in open(inputFilename)]

dictionary = corpora.Dictionary(texts)

totalNumberOfTokens = len(dictionary.keys())
print "Number of Tokens:" + str(totalNumberOfTokens)

dictionary.filter_extremes(no_above=no_above, no_below=no_below, keep_n=None);
# keep tokens that appear in more that 1% of documents
# keep tokens that don't appear in more than 80% of documents
print "Dictionary Created"

# remove stop words and rare words
stop_ids = [dictionary.token2id[stopword] for stopword in stopWords
            if stopword in dictionary.token2id]

# rare = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1] # filter words that do not appear frequently # I am not sure we need this

oneLetterWords = [tokenid for tokenid in dictionary.keys() if len(dictionary.get(tokenid)) == 1]
dictionary.filter_tokens(stop_ids + oneLetterWords)  # stop_ids + rare + oneLetterWords
dictionary.compactify()  # remove gaps in id sequence after words that were removed

numTokensAfterExtremeRemoval = len(dictionary.keys())
print "Number of TokensAfterExtremeRemoval:" + str(numTokensAfterExtremeRemoval)

# dictionary.save('strReviews.dict')  # dictionary = corpora.Dictionary.load('strReviews.dict')

# build corpus (vector representation of texts)
print "Preprocess Done"

corpus = [dictionary.doc2bow(text) for text in texts]

# corpus = dictionary.values . IS THIS EQUAL WITH

lda = ldamodel.LdaModel(corpus, id2word=dictionary,
                        num_topics=numTopics)  # model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary) # tfidf = models.TfidfModel(corpus); corpus_tfidf = tfidf[corpus]; lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

lda.save(
    resultsDir + "/" + 'lda_' + 'topics_' + str(numTopics) + '_above_' + str(no_above) + '_below_' + str(no_below) + '.model')

outputFile = open(
    resultsDir + "/" + 'topics_' + str(numTopics) + '_above_' + str(no_above) + '_below_' + str(no_below) + ".topics", 'w')

out = lda.print_topics(numTopics, 30)
for ind in out:
    for ind2 in ind:
        if isinstance(ind2, (int)):
            print >> outputFile, ind2
        else:
            print >> outputFile, ind2.encode('utf8')

outputFile.close()
