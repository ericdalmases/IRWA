import json
import random
from datetime import datetime
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
    
    fact_dayWeek_stored = []
    fact_browser_stored = []
    fact_os_stored = []
    start_time_doc = None
    fact_docTimes_stored = []



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
    
    def save_day_week(self, current_datetime: str) ->int:
        num_day_week = current_datetime.weekday()
        days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_week = days_week[num_day_week]

        for idx, (day, count) in enumerate(self.fact_dayWeek_stored):
            if day == day_week:
                self.fact_dayWeek_stored[idx] = (day_week, count + 1)
                break
        else:
            # If terms is not in the list, add it
            self.fact_dayWeek_stored.append((day_week, 1))

        self.fact_dayWeek_stored.sort(key=lambda x: x[1], reverse=True)

        self.to_pickle()
        return 0
    
    def save_browser(self, browser: str, ip) ->int:
        for idx, (b, count, ip_address) in enumerate(self.fact_browser_stored):
            if b == browser:
                if ip_address != ip:
                    self.fact_browser_stored[idx] = (b, count + 1, ip)
                break
        else:
            # If terms is not in the list, add it
            self.fact_browser_stored.append((browser, 1, ip))

        self.fact_browser_stored.sort(key=lambda x: x[1], reverse=True)

        self.to_pickle()
        return 0
    
    def save_os(self, os: str, ip) ->int:
        for idx, (operating_system, count, ip_address) in enumerate(self.fact_os_stored):
            if operating_system == os:
                if ip_address != ip:
                    self.fact_os_stored[idx] = (operating_system, count + 1, ip)
                break
        else:
            # If terms is not in the list, add it
            self.fact_os_stored.append((os, 1, ip))

        self.fact_os_stored.sort(key=lambda x: x[1], reverse=True)

        self.to_pickle()
        return 0
    
    def save_time_doc(self) ->int:
        if self.start_time_doc is not None:
            time_diff = (datetime.now() - self.start_time_doc)
            time_diff = round(time_diff.total_seconds())
            time_diff = min(time_diff, 180)
            print('time diff:', time_diff)
            for idx, (time, count) in enumerate(self.fact_docTimes_stored):
                if time == time_diff:
                    self.fact_docTimes_stored[idx] = (time_diff, count + 1)
                    break
            else:
                self.fact_docTimes_stored.append((time_diff, 1))
                max_value = max(item[0] for item in self.fact_docTimes_stored)
                existing_values = dict(self.fact_docTimes_stored)
                self.fact_docTimes_stored = [(i, existing_values.get(i, 0)) for i in range(1, max_value + 1)]
            
            self.fact_docTimes_stored.sort(key=lambda x: x[0], reverse=False)
            self.to_pickle()
            self.start_time_doc = None
        return 0
            
    def to_pickle(self):
        data = {}
        
        data['fact_clicks'] = self.fact_clicks_stored
        data['fact_queries'] = self.fact_queries_stored
        data['fact_searcher'] = self.fact_searcher_stored
        data['fact_terms'] = self.fact_terms_stored
        data['fact_dayWeek'] = self.fact_dayWeek_stored
        data['fact_browser'] = self.fact_browser_stored
        data['fact_os'] = self.fact_os_stored
        data['fact_docTimes'] = self.fact_docTimes_stored

        with open("./data/session_storage.pkl", 'wb') as f:
            pickle.dump(data, f)


    @staticmethod
    def from_pickle():
        try:
            with open("./data/session_storage.pkl", 'rb') as f:
                loaded_data = pickle.load(f)
            
            analytics = AnalyticsData()
            analytics.fact_clicks_stored = loaded_data['fact_clicks']
            analytics.fact_queries_stored = loaded_data['fact_queries']
            analytics.fact_searcher_stored = loaded_data['fact_searcher']
            analytics.fact_terms_stored = loaded_data['fact_terms']
            analytics.fact_dayWeek_stored = loaded_data['fact_dayWeek']
            analytics.fact_browser_stored = loaded_data['fact_browser']
            analytics.fact_os_stored = loaded_data['fact_os']
            analytics.fact_docTimes_stored = loaded_data['fact_docTimes']

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
