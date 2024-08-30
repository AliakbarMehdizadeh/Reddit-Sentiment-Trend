import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd


# Ensure you have the necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


class SentimentAnalyzer:
    def __init__(self):
        self.blob_analyzer = TextBlob
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        
        # Rejoin tokens into a single string
        cleaned_text = ' '.join(tokens)
        
        return cleaned_text

    def analyze_sentiment_for_person(self, text):
        blob = self.blob_analyzer(text)
        vader_score = self.vader_analyzer.polarity_scores(text)['compound']

        # Individual sentiment scores
        blob_polarity = blob.sentiment.polarity
        
        # Overall sentiment score as the average of the two
        overall_sentiment_score = (blob_polarity + vader_score) / 2.0

        return blob_polarity, vader_score, overall_sentiment_score

    def assess_sentiment_towards_people(self, text, kamala_keywords, trump_keywords):
        sentiment_results = {
            'kamala_blob_polarity': None,
            'kamala_vader_score': None,
            'kamala_overall_sentiment': None,
            'trump_blob_polarity': None,
            'trump_vader_score': None,
            'trump_overall_sentiment': None
        }
        
        # Check and analyze sentiment towards Kamala Harris
        kamala_mention = any(keyword in text.lower() for keyword in kamala_keywords)
        if kamala_mention:
            kamala_text = re.findall(rf'[^.]*\b(?:{"|".join(kamala_keywords)})\b[^.]*', text.lower())
            kamala_text = ' '.join(kamala_text)  # Combine all relevant sentences
            kamala_text = self.preprocess_text(kamala_text)
            blob_polarity, vader_score, overall_sentiment = self.analyze_sentiment_for_person(kamala_text)
            sentiment_results['kamala_blob_polarity'] = blob_polarity
            sentiment_results['kamala_vader_score'] = vader_score
            sentiment_results['kamala_overall_sentiment'] = overall_sentiment
        
        # Check and analyze sentiment towards Donald Trump
        trump_mention = any(keyword in text.lower() for keyword in trump_keywords)
        if trump_mention:
            trump_text = re.findall(rf'[^.]*\b(?:{"|".join(trump_keywords)})\b[^.]*', text.lower())
            trump_text = ' '.join(trump_text)  # Combine all relevant sentences
            trump_text = self.preprocess_text(trump_text)
            blob_polarity, vader_score, overall_sentiment = self.analyze_sentiment_for_person(trump_text)
            sentiment_results['trump_blob_polarity'] = blob_polarity
            sentiment_results['trump_vader_score'] = vader_score
            sentiment_results['trump_overall_sentiment'] = overall_sentiment
        
        return sentiment_results
