
from math import log
import nltk
import string

from nltk.corpus import wordnet as wn
from nltk.text import TextCollection

def contentexplore():
    a = {}
    return a


def attrexplore(corpus):
    # s = "in douglas r. stinson, editor,.proc. crypto 93,.lecture notes in computer science no. 773..pages 278-291..1994..avrim blum, merrick furst, michael kearns, and richard j. lipton..springer,.cryptographic primitives based on hard learning problems.."
    # ss = SenToken(raw=s)
    # print(ss)
    # for sent in ss:
    #     print(sent)

    nltkCorpus = TextCollection(corpus)
    print(nltkCorpus.idf(term='this'))


    print(idf(term='this',corpus=corpus))

    print(nltkCorpus.tf(term='this',text='this is sentence four'))
    print(tf_idf(term='this',doc='this is sentence four',corpus=corpus))
    fdist = nltk.FreqDist(WordTokener(sent=corpus[0]))
    print(fdist.tabulate())




def SenToken(raw):#分割成句子
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    sents =sent_tokenizer.tokenize(raw)
    return sents


def POSTagger(sents):
    taggedLine = [nltk.pos_tag(sent) for sent in sents]
    return taggedLine

def WordTokener(sent):#将单句字符串分割成词

        wordsInStr= nltk.word_tokenize(sent)
        return wordsInStr

def CleanLines(line):
    identify =string.maketrans('', '')
    delEStr =string.punctuation + string.digits #ASCII 标点符号，数字
#   cleanLine= line.translate(identify, delEStr) #去掉ASCII 标点符号和空格
    cleanLine =line.translate(identify,delEStr) #去掉ASCII 标点符号
    return cleanLine




def StemWords(cleanWordsList):
    stemWords=[]
#         porter = nltk.PorterStemmer()#有博士说这个词干化工具效果不好，不是很专业
#         result=[porter.stem(t) for t in cleanTokens]
    for words in cleanWordsList:
        stemWords += [[wn.morphy(w) for w in words]]
    return stemWords

def WordsToStr(stemWords):
        strLine=[]
        for words in stemWords:
           strLine +=[w for w in words]
        return strLine


def tf(term, doc, normalize=True):
    doc = doc.lower().split()
    if normalize:
        return doc.count(term.lower()) / float(len(doc))
    else:
        return doc.count(term.lower()) / 1.0


def idf(term, corpus):
    num_texts_with_term = len([True for text in corpus if term.lower() in text.lower().split()])

    # tf-idf calc incolves multiplying against a tf value less than 0, so it's
    # neccessary to return a value greater than 1 for consistent scoring.
    # (Multiplying two values less than 1 returns a value less then each of them.)
    try:
        return 1.0 + log(float(len(corpus)) / num_texts_with_term)
    except ZeroDivisionError:
        return 1.0


def tf_idf(term, doc, corpus):
    return tf(term, doc) * idf(term, corpus)