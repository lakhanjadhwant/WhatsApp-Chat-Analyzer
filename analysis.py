import emoji.unicode_codes
from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji 

def fetch_stats(selected_user,df):


    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    

    temp=df
    temp=temp[temp["Message"]!="<Media omitted>"]
    temp= temp[temp["Message"]!="null"]
    temp= temp[temp["Message"]!="This message was deleted"]
    temp= temp[temp["Message"]!="You deleted this message"]
    temp= temp[temp["Message"]!="image omitted"]

    #total number of messages
    total_msg=temp.shape[0]

    #total number of words
    total_words=[]
    for w in temp["Message"]:
        total_words.extend(w.split())

    #total number of media shared
    total_media = df[df["Message"]=="<Media omitted>"].shape[0]
    
    if total_media is None:
        total_media = df[df["Message"]=="‎image omitted"].shape[0]

    

    #total number of links shared
    extract = URLExtract()
    total_links=[]
    for msg in df["Message"]:
        total_links.extend(extract.find_urls(msg))

    # total view once media shared 
    total_view_once_media = df[df["Message"]=="null"].shape[0]

    # total deleted messages 
    total_del_msg = df[df["Message"].isin(["This message was deleted","You deleted this message"])].shape[0]

    
    return total_msg,len(total_words),total_media,len(total_links),total_view_once_media,total_del_msg


def active_user(df):
    x=df["User"].value_counts().head(3)
    
    pie_df=round(df["User"].value_counts()/df.shape[0]*100,0)
    pie_df=pie_df.reset_index()
    pie_df.columns = ["User", "Count"]
    
    pie_df=pie_df.head(7) 

    return x,pie_df

def create_wordcloud(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]



    temp=df
    temp=temp[temp["Message"]!="<Media omitted>"]
    temp= temp[temp["Message"]!="null"]
    temp= temp[temp["Message"]!="This message was deleted"]
    temp= temp[temp["Message"]!="You deleted this message"]

    # temp = temp[temp["Message"].str.strip() != ""]
    # Remove "<This message was edited>" from all messages in the "Message" column using .loc
    temp.loc[:, "Message"] = temp["Message"].str.replace("<This message was edited>", "", regex=False)
    

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc=wc.generate(temp["Message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):


    def contains_emoji(text):
    # Check if any emoji is present in the text using the emoji library
        return bool(emoji.emoji_list(text))

    if selected_user!="Overall":
        df=df[df["User"]==selected_user]



    temp=df
    temp=temp[temp["Message"]!="<Media omitted>"]
    temp= temp[temp["Message"]!="null"]
    temp= temp[temp["Message"]!="This message was deleted"]
    temp= temp[temp["Message"]!="You deleted this message"]


    # temp = temp[temp["Message"].str.strip() != ""]
    # Remove "<This message was edited>" from all messages in the "Message" column using .loc
    temp.loc[:, "Message"] = temp["Message"].str.replace("<This message was edited>", "", regex=False)
    
    

    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    top_words=[]

    # Tokenize and filter out stop words and emojis
    for msg in temp["Message"]:
        for word in msg.lower().split():
            # Check if the word is neither in stop words nor an emoji
            if word not in stop_words and not contains_emoji(word):
                top_words.append(word)

    Most_common_df=pd.DataFrame(Counter(top_words).most_common(10))
    Most_common_df.columns=["Word","Count"]
    
    return Most_common_df



def emojis(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]


    # Function to extract emojis using emoji library
    def extract_emojis(text):
        return [e['emoji'] for e in emoji.emoji_list(text)]

    # Extract emojis from all messages and flatten into a single list
    all_emojis = sum(df["Message"].apply(extract_emojis), [])

    emoji_counts = Counter(all_emojis).most_common(10)

    emoji_df = pd.DataFrame(emoji_counts, columns=["Emoji", "Count"])

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]



    df["Month_Name"]=df["Date"].dt.month
    timeline=df.groupby(["Year","Month_Name","Month"]).count()["Message"].reset_index()
    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i]+ " - " + str(timeline["Year"][i]))

    timeline["Time"]=time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]

    df["Only Date"]=df["Date"].dt.date

    daily_timeline=df.groupby(["Only Date"]).count()["Message"].reset_index()

    return daily_timeline


def most_active_day(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    
    df["Day Name"]=df["Date"].dt.day_name()
    day_name=df["Day Name"].value_counts().reset_index()

    return day_name
    

def most_active_month(selected_user,df):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    
    
    month_df=df["Month"].value_counts().reset_index()

    return month_df



        



    











        
   