from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji
extract=URLExtract()



def fetch_stats(selected_user,df):
    
    if selected_user !='Overall':
       df=df[df['name']==selected_user] 

    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())

     #fetch number of media messages
    num_media=df['message'].str.contains('<Media omitted>').sum()
    
    # fetch number of links
    from urlextract import URLExtract
    links=[]
    extractor=URLExtract()
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    
    
    return num_messages,len(words),num_media,len(links)

def most_busy_users(df):
    x=df['name'].value_counts().head()
    df=round((df['name'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','name':'percent'})
    return x,df

#  forming word cloud
def create_wordcloud(selected_user,df):
    if selected_user!= 'Overall':
       df=df[df['name']==selected_user] 

    wc=WordCloud(width=500,height=500,min_font_size=10, background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return wc

# most common words:
def most_common_words(selected_user,df):
    if selected_user!= 'Overall':
       df=df[df['name']==selected_user] 
    
    temp = df[~df['message'].str.contains(r'(?i)<Media omitted>')]
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    words_1=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words_1.append(word)

    most_common_df=pd.DataFrame(Counter(words_1).most_common(20))
    return most_common_df
# emoji analysis:

def most_common_emoji(selected_user,df):
    if selected_user!= 'Overall':
       df=df[df['name']==selected_user] 
    
    # create an empty dictionary to store the frequency of each emoji
    emoji_freq = {}

    # loop through each message in the dataframe and count the frequency of each emoji
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                if c in emoji_freq:
                    emoji_freq[c] += 1
                else:
                    emoji_freq[c] = 1

    # create a dataframe from the dictionary of emoji frequencies
    emoji_df = pd.DataFrame({'emoji': list(emoji_freq.keys()), 'frequency': list(emoji_freq.values())})

    # sort the dataframe by frequency in descending order
    emoji_df = emoji_df.sort_values(by=['frequency'], ascending=False)

    # display the dataframe
    return emoji_df

# Message frequency graph:
def message_frequency(selected_user,df):
    if selected_user!= 'Overall':
       df=df[df['name']==selected_user] 
    
    # create a datetime column using year and month columns
    df['datetime'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

    # create a time column using datetime column and format it as month-year
    df['time'] = df['datetime'].dt.strftime('%B-%Y')

    # select only the time and message_frequency columns and create a new dataframe
    new_df = df[['time', 'message']]

    # to make new dataframe 
    timeline=df.groupby(['time']).count()['message'].reset_index()
    return(timeline)
# daily timeline
def daily_timeline(selected_user,df):
    if selected_user!= 'Overall':
       df=df[df['name']==selected_user] 
    
    # create a datetime column using year and month columns
    df['datetime'] = pd.to_datetime(df[['year','month', 'day']])

    # create a time column using datetime column and format it as month-year
    df['time'] = df['datetime'].dt.strftime('%y-%m-%d')

    # select only the time and message_frequency columns and create a new dataframe
    new_df = df[['time', 'message']]

    # to make new dataframe 
    timeline=df.groupby(['time']).count()['message'].reset_index()
    return(timeline)

# week_activity
def week_activity_map(selected_user,df):
      if selected_user!= 'Overall':
         df=df[df['name']==selected_user] 
      
      return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
      if selected_user!= 'Overall':
         df=df[df['name']==selected_user] 
      
      return df['month_name'].value_counts()

# Activity heat map
def activity_heatmap(selected_user,df):
      if selected_user!= 'Overall':
         df=df[df['name']==selected_user] 
      
      user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
      return user_heatmap
    
    
