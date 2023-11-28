import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    fact_queries = []

    # statistics table 3
    fact_searcher = []

    def save_query_terms(self, terms: str) -> int:
        # Check if terms is already in the list
        for idx, (query, count) in enumerate(self.fact_queries):
            if query == terms:
                self.fact_queries[idx] = (query, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_queries.append((terms, 1))

        self.fact_queries.sort(key=lambda x: x[1], reverse=True)
        return random.randint(0, 100000)
    
    def save_search_engine(self, terms: str) -> int:
        for idx, (searcher, count) in enumerate(self.fact_searcher):
            if searcher == terms:
                self.fact_searcher[idx] = (searcher, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_searcher.append((terms, 1))

        self.fact_searcher.sort(key=lambda x: x[1], reverse=True)
        return 0


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
