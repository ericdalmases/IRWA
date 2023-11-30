import json
import random
import pickle


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])
    fact_clicks_stored = dict([])
    # statistics table 2
    fact_queries = []
    fact_queries_stored = []
    # statistics table 3
    fact_searcher = []
    fact_searcher_stored = []
    fact_terms_stored = []



    def save_clicked_docs(self, id: int) -> int:
        if id in self.fact_clicks.keys():
            self.fact_clicks[id] += 1
        else:
            self.fact_clicks[id] = 1

        if id in self.fact_clicks_stored.keys():
            self.fact_clicks_stored[id] += 1
        else:
            self.fact_clicks_stored[id] = 1

        self.to_pickle()
        return 0
    
    def save_query_terms(self, terms: str) -> int:
        # Check if terms is already in the list
        for idx, (query, count) in enumerate(self.fact_queries):
            if query == terms:
                self.fact_queries[idx] = (query, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_queries.append((terms, 1))
        
        for idx, (query, count) in enumerate(self.fact_queries_stored):
            if query == terms:
                self.fact_queries_stored[idx] = (query, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_queries_stored.append((terms, 1))
            
        self.fact_queries_stored.sort(key=lambda x: x[1], reverse=True)
        self.fact_queries.sort(key=lambda x: x[1], reverse=True)
        self.save_individual_terms(terms)

        self.to_pickle()
        return random.randint(0, 100000)
    
    def save_search_engine(self, terms: str) -> int:
        for idx, (searcher, count) in enumerate(self.fact_searcher):
            if searcher == terms:
                self.fact_searcher[idx] = (searcher, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_searcher.append((terms, 1))

        for idx, (searcher, count) in enumerate(self.fact_searcher_stored):
            if searcher == terms:
                self.fact_searcher_stored[idx] = (searcher, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_searcher_stored.append((terms, 1))

        self.fact_searcher_stored.sort(key=lambda x: x[1], reverse=True)
        self.fact_searcher.sort(key=lambda x: x[1], reverse=True)


        self.to_pickle()
        return 0
    
    def save_individual_terms(self, query:str) -> int:
        for term in query.split(" "):
            for idx, (existingTerm, count) in enumerate(self.fact_terms_stored):
                if term == existingTerm:
                    self.fact_terms_stored[idx] = (term, count + 1)
                    break
            else:
                # If terms is not in the list, add it
                self.fact_terms_stored.append((term, 1))

            self.fact_terms_stored.sort(key=lambda x: x[1], reverse=True)
        
        self.to_pickle()
        return 0
            
    def to_pickle(self):
        data = {}
        
        data['fact_clicks'] = self.fact_clicks_stored
        data['fact_queries'] = self.fact_queries_stored
        data['fact_searcher'] = self.fact_searcher_stored
        data['fact_terms'] = self.fact_terms_stored

        with open("./data/session_storage.pkl", 'wb') as f:
            pickle.dump(data, f)


    @staticmethod
    def from_pickle():
        try:
            with open("./data/session_storage.pkl", 'rb') as f:
                loaded_data = pickle.load(f)
            
            print(loaded_data)
            analytics = AnalyticsData()
            analytics.fact_clicks_stored = loaded_data['fact_clicks']
            analytics.fact_queries_stored = loaded_data['fact_queries']
            analytics.fact_searcher_stored = loaded_data['fact_searcher']
            analytics.fact_terms_stored = loaded_data['fact_terms']

            return analytics
        except:
            print("Storage analytics not found")
            return AnalyticsData()


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
