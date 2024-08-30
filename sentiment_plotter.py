import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class SentimentPlotter:
    def __init__(self, comments_list_by_post: pd.DataFrame, subreddit_names_list: list):
        self.comments_list_by_post = comments_list_by_post
        self.subreddit_names_list = subreddit_names_list
        sns.set(style="dark")
        self.colors = {
            subreddit_names_list[0]: 'blue',
            subreddit_names_list[1]: 'green',
            subreddit_names_list[2]: 'red'
        }

    def plot_sentiment_trends(self):
        # Create a figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), sharex=True, sharey=True)
        
        # Plot sentiment trends for each subreddit
        for subreddit in self.subreddit_names_list:
            # Filter data for the current subreddit
            subreddit_data = self.comments_list_by_post[self.comments_list_by_post['subreddit'] == subreddit]
            
            # Resample and calculate daily sentiment
            numeric_data = subreddit_data.select_dtypes(include='number').resample('D').mean()
            
            # Plot Kamala Harris sentiment in the first subplot
            ax1.plot(numeric_data.index, numeric_data['kamala_overall_sentiment'], label=f'r/{subreddit}', color=self.colors.get(subreddit, 'black'))
            # ax1.plot(numeric_data.index, numeric_data['kamala_blob_polarity'], label=f'{subreddit}_kamala_blob_polarity', color=self.colors.get(subreddit, 'black'), linestyle='--', alpha=0.5)
            # ax1.plot(numeric_data.index, numeric_data['kamala_vader_score'], label=f'{subreddit}_kamala_vader_score', color=self.colors.get(subreddit, 'black'), linestyle=':', alpha=0.5)

            # Plot Trump sentiment in the second subplot
            ax2.plot(numeric_data.index, numeric_data['trump_overall_sentiment'], label=f'r/{subreddit}', color=self.colors.get(subreddit, 'black'))
            # ax2.plot(numeric_data.index, numeric_data['trump_blob_polarity'], label=f'{subreddit}_trump_blob_polarity', color=self.colors.get(subreddit, 'black'), linestyle='--', alpha=0.5)
            # ax2.plot(numeric_data.index, numeric_data['trump_vader_score'], label=f'{subreddit}_trump_vader_score', color=self.colors.get(subreddit, 'black'), linestyle=':', alpha=0.5)
        
        # Set labels and titles
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sentiment Score')
        ax1.set_title('Kamala Harris Sentiment Trends')
        ax1.legend(loc='best')
        ax1.grid(True)  # Add grid to the first subplot
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Sentiment Score')
        ax2.set_title('Donald Trump Sentiment Trends')
        ax2.legend(loc='best')
        ax2.grid(True)  # Add grid to the second subplot
        
        # Save the figure
        if not os.path.exists('result'):
            os.makedirs('result')
        plt.savefig('result/sentiment_trends.png')
        # Adjust layout
        plt.tight_layout()
        plt.show()
        plt.close()

    def plot_correlation_matrix(self):
        # Initialize a DataFrame to store all time series
        combined_time_series = pd.DataFrame()

        for subreddit in self.subreddit_names_list:
            # Filter data for the current subreddit
            subreddit_data = self.comments_list_by_post[self.comments_list_by_post['subreddit'] == subreddit]
            
            # Resample and calculate daily sentiment
            numeric_data = subreddit_data.select_dtypes(include='number').resample('D').mean()

            # Store time series in the combined DataFrame
            combined_time_series[f'r/{subreddit}: kamala'] = numeric_data['kamala_overall_sentiment']
            combined_time_series[f'r/{subreddit}: trump'] = numeric_data['trump_overall_sentiment']

        # Calculate the Correlation Matrix
        correlation_matrix = combined_time_series.corr()

        # Visualize the Correlation Matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix of Sentiment Scores')
         
        # Save the figure
        if not os.path.exists('result'):
            os.makedirs('result')
        plt.savefig('result/corr_matrix.png')
        plt.show()
        plt.close()

        # Display the correlation matrix
        print('check result folder for results')
