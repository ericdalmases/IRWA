import os
from json import JSONEncoder
import json

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session
from flask import request
import pickle
import requests
from datetime import datetime

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Tweet, StatsDocument
from myapp.search.search_engine import SearchEngineTfIdf, SearchEngineOurScore, SearchEngineWord2Vec
from myapp.search.algorithms import TextProcessor


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'


# instantiate our in memory persistence
analytics_data = AnalyticsData.from_pickle()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/data/tweets_test.json"

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)

print("Loading index prom pickle...")
with open('saved_steps.pkl', 'rb') as file:
    index, tf, df, idf, title_index = pickle.load(file)
print("Index loaded")

# instantiate our search engine
search_engine_tfidf = SearchEngineTfIdf(
    corpus=corpus,
    index=index,
    tf=tf,
    idf=idf,
    title_index = title_index
)

custom_scores = {}
for doc_id in corpus.keys():
  custom_scores[doc_id] = corpus[doc_id].getCustomScore()

search_engine_popularity = SearchEngineOurScore(
    corpus=corpus,
    index=index,
    scores=custom_scores
)

token_tweets = []
for doc_id in corpus.keys():
    token_tweets.append(TextProcessor.process(corpus[doc_id].description))

search_engine_word2vec = SearchEngineWord2Vec(
    corpus=corpus,
    token_tweets=token_tweets
)

# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2023 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")



@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']
    session['last_search_query'] = search_query
    search_method = request.form['search-method']
    search_id = analytics_data.save_query_terms(search_query)
    analytics_data.save_search_engine(search_method)
    
    current_datetime = datetime.now()
    analytics_data.save_day_week(current_datetime)

    if(search_method == "TF-IDF"):
        results = search_engine_tfidf.search(search_query, search_id)
    elif(search_method == "Popularity based"):
        results = search_engine_popularity.search(search_query, search_id)
    elif((search_method == "Word2Vec")):
        results = search_engine_word2vec.search(search_query, search_id)
    else:
        return


    found_count = len(results)
    session['last_found_count'] = found_count

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = int(request.args["id"])
    p1 = int(request.args["search_id"])  # transform to Integer
    p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    analytics_data.save_clicked_docs(clicked_doc_id)
    # store data in statistics table 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))
    output_tweet = corpus[clicked_doc_id]
    print(output_tweet)

    return render_template('doc_details.html', output_tweet=output_tweet, page_title=f"Details of {output_tweet.title}")


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """

    docs = []

    for doc_id in analytics_data.fact_clicks:
        row: Tweet = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    # simulate sort by ranking
    docs.sort(key=lambda doc: doc.count, reverse=True)

    browser = request.headers.get('User-Agent')
    os = request.user_agent.platform

    current_datetime = datetime.now()
    # Get current time of the day
    current_time = current_datetime.strftime('%H:%M:%S')

    # Get current date
    current_date = current_datetime.strftime('%d/%m/%Y')
    print(request.remote_addr)
    ip_address = "Unknown"
    country = "Unknown"
    city = "Unknown"

    # Get IP address using an external service
    try:
        ip_info = requests.get('https://api64.ipify.org?format=json').json()
        ip_address = ip_info['ip']
        country = ip_info['location']['country']
        city = ip_info['location']['city']
    except Exception as e:
        print('Error fetching IP information:', e)

    print(analytics_data.fact_queries)

    return render_template(
        'stats.html', 
        clicks_data=docs,
        queries= analytics_data.fact_queries,
        browser = browser,
        os = os,
        current_time = current_time,
        current_date = current_date,
        ip_address = ip_address,
        country = country,
        city = city
        )


@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    for doc_id in analytics_data.fact_clicks_stored.keys():
        d: Tweet = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks_stored[doc_id])
        visited_docs.append(doc)

    visited_docs_json = []
    # simulate sort by ranking
    for doc in visited_docs: visited_docs_json.append(doc.to_json())
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)
    words = []
    
    suma = sum([t[1] for t in analytics_data.fact_terms_stored])

    for word in analytics_data.fact_terms_stored:
        words.append({'word': word[0], 'size': 100*word[1]/suma})
        
    print(analytics_data.fact_dayWeek_stored)
   
    return render_template('dashboard.html', visited_docs=visited_docs_json, searched_queries=analytics_data.fact_queries_stored,
                           search_method=analytics_data.fact_searcher_stored, searched_terms=analytics_data.fact_terms_stored, words=words,
                           daysWeek=analytics_data.fact_dayWeek_stored)


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
