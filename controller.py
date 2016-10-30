from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SubmitField, SelectField, DecimalField, TextField
from wtforms.validators import Required
import simplejson
import sys
import logging
import pickle

import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd
import numpy as np
from textblob import TextBlob, Word

import scipy as sp
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from nltk.stem.snowball import SnowballStemmer
from ipywidgets import widgets



# Load Twitter Word List for Candidates
hrc_twitter_words = pd.read_csv('hills_twitter_words.csv')
dt_twitter_words = pd.read_csv('lil_donnie_twitter_words.csv')


# Initialize Flask App
app = Flask(__name__)

# Initialize Form Class
class theForm(Form):
    user_word = TextField('Word:', validators=[Required()])
    submit = SubmitField('Submit')



# function to get word count for HRC
def hrc_word_count(x):
    z = x.lower()
    df = hrc_twitter_words[hrc_twitter_words.Word == z]
    print df.shape[0], "HILLAR"
    if df.shape[0]:
        return int(df.Times_Used)
    return None

# function to get word count for dt
def dt_word_count(x):
    z = x.lower()
    df = dt_twitter_words[dt_twitter_words.Word == z]
    print df.shape[0], "TRUMP"
    if df.shape[0]:
        return int(df.Times_Used)
    return None


@app.route('/', methods=['GET', 'POST'])
def model():
    form = theForm(csrf_enabled=False)
    if form.validate_on_submit():  # activates this if when i hit submit!
        # Retrieve values from form
        session['user_word'] = form.user_word.data
        session['user_word_cap'] = session['user_word'].capitalize()
        y = session['user_word']

        # Use word count functions to get # of times word used for each
        hrc_usage = hrc_word_count(y)
        dt_usage = dt_word_count(y)
        session['hrc_usage'] = hrc_usage
        session['dt_usage'] = dt_usage
        print hrc_usage, dt_usage


        return redirect(url_for('model'))
        # return dt_usage
        # return hrc_usage

    return render_template('model.html', form=form, **session)

@app.route('/projects/')
def projects():
    return 'The project page'

# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.secret_key = 'super_secret_key'

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)
