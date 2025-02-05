import re
import pandas as pd
from datetime import datetime
from dateutil import parser


def create_dataframe(data):
        
    if data[0]=="[":
        df=create_dataframe_iphone(data)
    else:
        df=create_dataframe_android(data)

    return df



    


def check_format(df):
    pattern=r"(\d{1,2}\/\d{1,2})"
    naya=[]

    for date in df["Date"]:
            entry=re.split(pattern,date,maxsplit=1)
            naya.append(entry[1].split("/"))

    df_format=pd.DataFrame(naya, columns=["col1","col2"])
    df_format["col1"] = df_format["col1"].astype(int) 
    df_format["col2"] = df_format["col2"].astype(int) 

    tf=None

    for val1 in df_format["col1"]:
        if val1 > 12:
            tf=True
            break
        else:
            tf=False

    
    return tf





def create_dataframe_android(data):
    rows=[line.split(" - ",1) for line in data.split("\n") if " - " in line]
    df=pd.DataFrame(rows,columns=["Date","Text"])
    user=[]
    message=[]

    for msg in df["Text"]:
        entry=re.split(r"([^:]+):\s",msg,maxsplit=1)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("Group Notification")
            message.append(entry[0])

    


    df["User"]=user
    df["Message"]=message
    df.drop(columns=["Text"],inplace=True)

    samp=df.sample(100)

    day_value=check_format(samp)

    if day_value:
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=True)
    else:
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=False)
    
    
    
    df["Year"]=df["Date"].dt.year
    df["Month"]=df["Date"].dt.month_name()
    df["Day"]=df["Date"].dt.day
    df["Hour"]=df["Date"].dt.hour
    df["Minute"]=df["Date"].dt.minute
    # df.drop(columns=["Date"],inplace=True)

    df=df[df["User"]!="Group Notification"]


    return df



def create_dataframe_iphone(data):
        
    rows=[line.split("] ",1) for line in data.split("\n") if "] " in line]
    df=pd.DataFrame(rows,columns=["Date","Text"])
    df["Date"] = df["Date"].str.replace("[", "", regex=False)
    df["Date"] = df["Date"].str.replace("‎", "", regex=True)
    


    user=[]
    message=[]

    for msg in df["Text"]:
        entry=re.split(r"([^:]+):\s",msg,maxsplit=1)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("Group Notification")
            message.append(entry[0])

    


    df["User"]=user
    df["Message"]=message
    df.drop(columns=["Text"],inplace=True)

    samp=df.sample(100)

    day_value=check_format(samp)

    if day_value:
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=True)
    else:
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",dayfirst=False)
    
    
    
    df["Year"]=df["Date"].dt.year
    df["Month"]=df["Date"].dt.month_name()
    df["Day"]=df["Date"].dt.day
    df["Hour"]=df["Date"].dt.hour
    df["Minute"]=df["Date"].dt.minute
    # df.drop(columns=["Date"],inplace=True)

    df=df[df["User"]!="Group Notification"]


    return df