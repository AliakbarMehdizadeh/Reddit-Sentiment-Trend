from credentials import CLIENT_ID, CLIENT_SECRET
from config import TOP_POSTS_TIME_FILTER, MAXIMUM_POSTS_PER_SUBREDDIT,SUBREDDIT_NAMES_LIST, kamala_keywords, trump_keywords
from data_gatherer import DataGatherer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_plotter import SentimentPlotter


import pandas as pd

if __name__ == "__main__":
    
    # Initialize DataGatherer
    data_gatherer = DataGatherer(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        subreddit_names_list=SUBREDDIT_NAMES_LIST,
        top_posts_time_filter=TOP_POSTS_TIME_FILTER,
        maximum_posts_per_subreddit=MAXIMUM_POSTS_PER_SUBREDDIT
    )
    
    # Retrieve comments
    comments_list_by_post = data_gatherer.get_comments_list_by_post()
    
    # Initialize SentimentAnalyzer
    analyzer = SentimentAnalyzer()
    
    # Apply sentiment analysis
    sentiment_features = comments_list_by_post['comment'].apply(
        lambda text: analyzer.assess_sentiment_towards_people(text, 
kamala_keywords, trump_keywords)
    ).apply(pd.Series)
    
    # Concatenate sentiment features to original DataFrame
    comments = pd.concat([comments_list_by_post, sentiment_features], 
axis=1)
    
    # Convert 'created_time' to datetime and set as index
    comments['date'] = pd.to_datetime(comments['created_time'], unit='s')
    comments.set_index('date', inplace=True)
    
    # Optionally, drop 'created_time' column if it's no longer needed
    comments.drop(columns=['created_time'], inplace=True)
    
    # Initialize SentimentPlotter
    plotter = SentimentPlotter(comments, SUBREDDIT_NAMES_LIST)
    
    # Plot sentiment trends
    plotter.plot_sentiment_trends()
    
    # Plot and print correlation matrix
    plotter.plot_correlation_matrix()
