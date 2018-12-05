from flask import render_template, request, Blueprint
from ttb.models import Post, Comment
from flask_bootstrap import Bootstrap
from textblob import TextBlob, Word
from ttb.main.forms import InputTextForm
from datetime import datetime

import random
import logging

main = Blueprint('main', __name__)

@main.route("/")


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts=posts, current_time=datetime.utcnow())




@main.route('/api/sentiment',methods=['POST'])
def sentiment():
	text = TextBlob(request.form['message'])
	response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity}
	return jsonify(response)



def track_event(category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': '555',
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
    }

    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)

    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()


@main.route('/')
def track_example():
    track_event(
        category='Example',
        action='test action')
    return 'Event tracked.'


@main.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
















def analyse():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        #NLP Stuff
        blob = TextBlob(rawtext)
        received_text2 = blob
        blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
        number_of_tokens = len(list(blob.words))
        # Extracting Main Points
        nouns = list()
        for word, tag in blob.tags:
            if tag == 'NN':
                nouns.append(word.lemmatize())
                len_of_words = len(nouns)
                rand_words = random.sample(nouns,len(nouns))
                final_word = list()
                for item in rand_words:
                    word = Word(item).pluralize()
                    final_word.append(word)
                    summary = final_word
                    end = time.time()
                    final_time = end-start
        return render_template('analytics.html',received_text = received_text2,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)
