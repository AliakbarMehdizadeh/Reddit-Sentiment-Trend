import praw
from typing import List, Dict
import sys
import pandas as pd 

class DataGatherer:

    def __init__(self, client_id: str, client_secret: str, 
subreddit_names_list: List[str], 
                 maximum_posts_per_subreddit: int, top_posts_time_filter: 
str):
        self.subreddit_names_list = subreddit_names_list
        self.maximum_posts_per_subreddit = maximum_posts_per_subreddit
        self.top_posts_time_filter = top_posts_time_filter
        self.reddit_client = praw.Reddit(client_id=client_id,
                                         client_secret=client_secret,
                                         user_agent="user_agent")
        self.comments_list = []

    def get_comments_list_by_post(self) -> pd.DataFrame:
        
        
        for subreddit_name in self.subreddit_names_list:
            
            retrieved_posts_count = 0
            
            subreddit = self.reddit_client.subreddit(subreddit_name)
            top_posts = subreddit.top(time_filter=self.top_posts_time_filter, 
limit=self.maximum_posts_per_subreddit)

            current_subreddit_retrieved_posts_count = 0
            
            for post in top_posts:
                post_id = post.id
                post_created_time = post.created_utc

                post.comments.replace_more(limit=0)

                for comment in post.comments.list():
                    comment_author = comment.author
                    if comment_author and comment_author.name != "AutoModerator":
                        self.comments_list.append({
                            'comment': comment.body,
                            'post_id': post_id,
                            'created_time': comment.created_utc,
                            'subreddit': subreddit_name,
                            'author_id': comment_author.name  # Store author ID
                        })

                retrieved_posts_count += 1
                current_subreddit_retrieved_posts_count += 1
                
                progress_message = f"Retrieved posts from r/{subreddit_name}: {current_subreddit_retrieved_posts_count}"
    
                # Print the progress message with carriage return to overwrite the line
                sys.stdout.write(f"\r{progress_message}")
                
                # Flush the output to ensure it appears immediately
                sys.stdout.flush()
                
                if current_subreddit_retrieved_posts_count >= self.maximum_posts_per_subreddit:
                    break                
                
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(self.comments_list)
        
        # Convert 'created_time' from UNIX timestamp to datetime
        df['created_time'] = pd.to_datetime(df['created_time'], unit='s')
        
        return df
