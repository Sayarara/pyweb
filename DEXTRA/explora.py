
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

def contentexplore():
    a = {}
    return  a

def attrexplore(corpus):
    vectorizer = CountVectorizer()
    trnsformer = TfidfTransformer()
    tfidf = trnsformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    for i in range(len(weight)):
        for j in range(len(word)):
            print(word[j],weight[i][j])


