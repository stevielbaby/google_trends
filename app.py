from flask import Flask, render_template, request
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

def get_pytrends_data(keyword, region):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo=region, gprop='')
    return pytrends

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    keyword = request.form['keyword']
    region = request.form['region']
    
    pytrends = get_pytrends_data(keyword, region)
    
    interest_by_region_df = pytrends.interest_by_region().reset_index()
    related_queries = pytrends.related_queries()
    interest_over_time = pytrends.interest_over_time().reset_index()
    top_related_topics = pytrends.related_topics()[keyword]['top']
    rising_related_topics = pytrends.related_topics()[keyword]['rising']

    data = {
        'interest_by_region': interest_by_region_df.to_dict(orient='records'),
        'related_queries': related_queries,
        'interest_over_time': interest_over_time.to_dict(orient='records'),
        'top_related_topics': top_related_topics.to_dict(orient='records'),
        'rising_related_topics': rising_related_topics.to_dict(orient='records')
    }

    return render_template('results.html', keyword=keyword, region=region, data=data)

@app.route('/interest_by_region/<keyword>/<region>')
def interest_by_region(keyword, region):
    pytrends = get_pytrends_data(keyword, region)
    interest_by_region_df = pytrends.interest_by_region().reset_index()
    return interest_by_region_df.to_json(orient='records')

@app.route('/related_queries/<keyword>/<region>')
def related_queries(keyword, region):
    pytrends = get_pytrends_data(keyword, region)
    related_queries = pytrends.related_queries()
    return related_queries

@app.route('/interest_over_time/<keyword>/<region>')
def interest_over_time(keyword, region):
    pytrends = get_pytrends_data(keyword, region)
    interest_over_time = pytrends.interest_over_time().reset_index()
    return interest_over_time.to_json(orient='records')

@app.route('/related_topics/<keyword>/<region>')
def related_topics(keyword, region):
    pytrends = get_pytrends_data(keyword, region)
    top_related_topics = pytrends.related_topics()[keyword]['top']
    rising_related_topics = pytrends.related_topics()[keyword]['rising']
    return {
        'top_related_topics': top_related_topics.to_json(orient='records'),
        'rising_related_topics': rising_related_topics.to_json(orient='records')
    }

if __name__ == '__main__':
    app.run(debug=True)
