from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
from scipy.sparse import csr_matrix


def testtfidfcosine():
    twenty = fetch_20newsgroups()
    tfidf = TfidfVectorizer().fit_transform(twenty.data)  # 11314x130088 sparse matrix
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten() # first, 0:1,  second, 1:2
    print(cosine_similarities)
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    print(related_docs_indices)
    print(cosine_similarities[related_docs_indices])
    #print(twenty.data[0])
    print(len(twenty.data))  # 11314

def tfidfcosine(data,seed):
    tfidf = TfidfVectorizer().fit_transform(data)
    cosine_similarities = linear_kernel(tfidf[seed:seed+1], tfidf).flatten()
    #related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    return cosine_similarities

def testMatrix1():
    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])
    a = csr_matrix((data, (row, col)), shape=(3, 3)).toarray()
    print(a)
    print(a[1:2])

def testMatrix2():
    indptr = np.array([0, 2, 3, 6])
    indices = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])
    a = csr_matrix((data, indices, indptr), shape=(3, 3)).toarray()

    print(a)

#testMatrix1()
#testtfidfcosine()