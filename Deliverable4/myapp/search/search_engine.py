
from myapp.search.objects import ResultItem, Tweet
from myapp.search.algorithms import search_in_corpus, search_custom, TextProcessor

import gensim
from gensim.models import Word2Vec, KeyedVectors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SearchEngineTfIdf:
    """educational search engine"""
    def __init__(self, corpus, index, tf, idf, title_index):
        self.corpus = corpus
        self.index = index
        self.tf = tf
        self.idf = idf
        self.title_index = title_index

    def search(self, search_query, search_id):
        print("Search query:", search_query)

        doc_scores = search_in_corpus(search_query, self.index, self.tf, self.idf, self.title_index)

        # AND condition of the search
        query_tokens = TextProcessor.process(search_query)
        query_tokens = set(query_tokens)
        filtered_docs_scores = [pair for pair in doc_scores if len(query_tokens.intersection(set(TextProcessor.process(self.corpus[pair[1]].description)))) >= len(query_tokens)]

        res = []
        
        for pair in doc_scores:
            docId = pair[1]
            score = pair[0]
            item: Tweet = self.corpus[docId]
            res.append(ResultItem(item.id, item.title, item.description, item.doc_date,"doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), score))
        
    
        return res
    

class SearchEngineOurScore:
    """educational search engine"""
    def __init__(self, corpus, index, scores):
        self.corpus = corpus
        self.index = index
        self.custom_scores = scores

    def search(self, search_query, search_id):
        print("Search query:", search_query)

        doc_scores = search_custom(search_query, self.index, self.custom_scores)

        # AND condition of the search
        query_tokens = TextProcessor.process(search_query)
        query_tokens = set(query_tokens)
        filtered_docs_scores = [pair for pair in doc_scores if len(query_tokens.intersection(set(TextProcessor.process(self.corpus[pair[1]].description)))) >= len(query_tokens)]

        res = []
        
        for pair in filtered_docs_scores:
            docId = pair[1]
            score = pair[0]
            item: Tweet = self.corpus[docId]
            res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                                "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), score))
        
        return res
    
def average_vector(tokens, model):
    # Filter out words that are not in the vocabulary
    tokens = [word for word in tokens if word in model.wv.key_to_index]

    if len(tokens) == 0:
        return np.zeros(model.wv.vector_size)

    # Calculate the average vector for the given tokens
    vector_sum = np.zeros(model.wv.vector_size)
    for word in tokens:
        vector_sum += model.wv[word]

    return vector_sum / len(tokens)

class SearchEngineWord2Vec:
    """educational search engine"""
    def __init__(self, corpus, token_tweets):
        self.corpus = corpus
        self.model = Word2Vec(token_tweets, min_count = 1, vector_size = 100, window = 5)

    def search(self, search_query, search_id):
        print("Search query:", search_query)

        query_tokens = TextProcessor.process(search_query)
        query_embedded = average_vector(query_tokens, self.model)
        doc_scores = []
        res = []

        # AND condition of the search
        query_tokens = set(query_tokens)
        filtered_docs = [docId for docId in self.corpus if len(query_tokens.intersection(set(    TextProcessor.process(self.corpus[docId].description)))) >= len(query_tokens)]

        for docId in filtered_docs:
            tweet_embedded = average_vector(self.corpus[docId].description, self.model) # We compute the embedding of the tweet
            doc_scores.append([
                cosine_similarity(np.array(query_embedded).reshape(1, -1), np.array(tweet_embedded).reshape(1, -1))[0][0], docId])
        
        doc_scores = sorted(doc_scores, key=lambda x: x[0], reverse=True)
        print(doc_scores)


        for pair in doc_scores:
            docId = pair[1]
            score = pair[0]
            item: Tweet = self.corpus[docId]
            res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                                "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), score))
            
        return res
