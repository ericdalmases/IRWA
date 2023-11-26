from collections import defaultdict
from array import array
import math
import numpy as np
import collections
from numpy import linalg as la
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('stopwords')
from nltk.corpus import stopwords
import regex as re

class TextProcessor():
  @staticmethod
  def process(input: str) -> str:
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    output = input.lower() ## Transform in lowercase
    output = re.sub(r"(https?://\S+)|[^\w\s@🇺🇸🇺🇦🇷🇺🇨🇳🇪🇺🇹🇷]|\n|#", ' ', output) # Delete URLs, all symbols that are not mentions, hashtags or important flags (US, UA, RU)
    output = output.strip() # Delete spaces in front / at the end of the text ()
    output = re.split(r'\s+', output) # Split the text by spaces (same as output.split but considers a set of blank spaces as one)
    output = [i for i in output if i not in stop_words] # and .isalpha()
    output = [stemmer.stem(i) for i in output]
    return output
  
########################################################################
###################   CLASSICAL TF-IDF #################################
########################################################################
  
def rank_documents(terms, docs, index, idf, tf, title_index):
    """
    Perform the ranking of the results of a search based on the tf-idf weights

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    title_index -- mapping between page id and page title

    Returns:
    Print the list of ranked documents
    """

    # I'm interested only on the element of the docVector corresponding to the query terms
    # The remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.

    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex]= query_terms_count[term]/ query_norm * idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]  # TODO: check if multiply for idf

    doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)
    return doc_scores

def search_tf_idf(query, index, idf, tf, title_index):
    """
    output is the list of documents that contain any of the query terms.
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = TextProcessor.process(query) # We use our custom processor for the text to match the processing performed to the tweets
    docs = set()
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs=[posting[0] for posting in index[term]]

            # docs = docs Union term_docs
            docs = docs.union(term_docs)
        except:
            #term is not in index
            pass
    docs = list(docs)
    ranked_docs = rank_documents(query, docs, index, idf, tf, title_index)
    return ranked_docs



def search_in_corpus(query, index, tf, idf, title_index):
    
    ranked_docs = search_tf_idf(query, index, idf, tf, title_index)

    return ranked_docs


########################################################################
###################   OUR SCORE BASED ON POPULARITY ####################
########################################################################

def rank_documents_custom(terms, docs, index, custom_scores):
    """
    Perform the ranking of the results of a search based on the custom scores

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    custom_scores -- custom scores for each document

    Returns:
    Print the list of ranked documents
    """

    # I'm interested only in the element of the docVector corresponding to the query terms
    # The remaining elements would become 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms))  # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.
    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  # termIndex is the index of the term in the query
        if term not in index:
            continue

        # Compute the custom score for the query term
        query_vector[termIndex] = query_terms_count[term] / query_norm

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):
            # Check if the doc is in the list of documents to rank
            if doc in docs:
                doc_vectors[doc][termIndex] = custom_scores[doc] # Use the custom score directly

    # Calculate the score of each doc
    # compute the cosine similarity between queryVector and each docVector:
    # HINT: you can use the dot product because in case of normalized vectors it corresponds to the cosine similarity
    # see np.dot
    doc_scores = [[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)

    return doc_scores

def search_custom(query, index, custom_scores):
    """
    output is the list of documents that contain any of the query terms.
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = TextProcessor.process(query) # We use our custom processor for the text to match the processing performed to the tweets
    docs = set()
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs=[posting[0] for posting in index[term]]

            # docs = docs Union term_docs
            docs = docs.union(term_docs)
        except:
            #term is not in index
            pass
    docs = list(docs)
    ranked_docs = rank_documents_custom(query, docs, index, custom_scores)
    return ranked_docs


