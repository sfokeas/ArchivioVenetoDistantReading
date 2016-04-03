import string

from gensim import corpora
from gensim.models import ldamodel
from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer
from nltk.tokenize import TreebankWordTokenizer

excludeSet = string.punctuation + ""
totalNumberOfWords = 8255414
totalNumberOfDocuments = 98

stemmer = ItalianStemmer()


def preprocessLine(strLine):
    strLine = strLine.decode('utf8').lower()
    strLine = ''.join(stemmer.stem(ch) for ch in strLine if ch not in set(excludeSet)) #todo put a print just to now the progress of the algo
    return strLine


# translate({i:" " for i in string.punctuation.replace("'",'')})

# Why split sentences???


# Build dictionary
stopWords = set(stopwords.words('italian'))
tokenizer = TreebankWordTokenizer()
dictionary = corpora.Dictionary(
    tokenizer.tokenize(
        preprocessLine(line)
    ) for line in open('one_journal_per_line'))

# statistics: how many words in the dictionary. These are the number of difference words in the documents.
# statistics: wc * to find out the number of words,lines,characters inside journal.

totalNumberOfTokens = len(dictionary.keys())  #save pure dictionary!

dictionary.filter_extremes(no_below=totalNumberOfDocuments * 0.01, no_above=0.8, keep_n=None);
# keep tokens that appear in more that 1% of documents
# keep tokens that don't appear in more than 80% of documents


# remove stop words and rare words
stop_ids = [dictionary.token2id[stopword] for stopword in stopWords
            if stopword in dictionary.token2id]

# filter words that do not appear frequently
rare = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]

oneLetterWords = [tokenid for tokenid in dictionary.keys() if len(dictionary.get(tokenid)) == 1] # doesn't work. goal was to remove one leter words

dictionary.filter_tokens(stop_ids + rare)
dictionary.compactify()  # remove gaps in id sequence after words that were removed

numTokensAfterExtremeRemoval = len(dictionary.keys())

dictionary.save('strReviews.dict')

dictionary = corpora.Dictionary.load('strReviews.dict')


# build corpus (vector representation of texts)


class MyCorpus(object):
    def __iter__(self):
        for line in open('one_journal_per_line'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(tokenizer.tokenize(preprocessLine(line)))


corpus = MyCorpus()

# build LDA

lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=20) # model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary) # tfidf = models.TfidfModel(corpus); corpus_tfidf = tfidf[corpus]; lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

# final output is topics... topics are coefficients over a set of words...

lda.save('lda_journals.model')  # <<---- don't forget to execute this on the console!

# get topics for each document
for line in open('one_journal_per_line'):
    print lda.get_document_topics(dictionary.doc2bow(tokenizer.tokenize(preprocessLine(line))))

# lda2 = ldamodel.LdaModel.load

# ---- example code

# import nltk.data
# >>> tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
# >>> tokenizer.tokenize(para)
# ['Hello World.', "It's good to see you.", 'Thanks for buying this book.']


topics = open('topic.txt', 'w')
out = lda.print_topics(20, 10)
for ind in out:
    for ind2 in ind:
        if isinstance(ind2, (int)):
            print >> topics, ind2
        else:
            print >> topics, ind2.encode('utf8')

topics.close()
