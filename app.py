import streamlit as st
from preprocess import create_dataframe
from analysis import fetch_stats, active_user,create_wordcloud,most_common_words,emojis,monthly_timeline,daily_timeline, most_active_day, most_active_month
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit Page Configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("📂 Choose a file")

if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):

        # Load Data
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = create_dataframe(data)
        
        # Display DataFrame
        # st.markdown("### 📜 Chat Data Preview")
        # st.dataframe(df)

        # User Selection
        user_list = df["User"].unique().tolist()
        
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("🔍 Show Analysis for", user_list)

        if st.sidebar.button("📊 Show Analysis"):
            msg_count, words_count, media_count, links_count, view_once_media_count, del_msg_count= fetch_stats(selected_user, df)

            # **📌 Stats Section**
            st.markdown("## 📊 Chat Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.metric(label="💬 Messages", value=msg_count)
            with col2:
                st.metric(label="📝 Words", value=words_count)
            with col3:
                st.metric(label="🫣 View Once Media", value=view_once_media_count)
            with col4:
                st.metric(label="📷 Media Files", value=media_count)
            with col5:
                st.metric(label="🔗 Links Shared", value=links_count)
            with col6:
                st.metric(label="🙊 Deleted Messages", value=del_msg_count)
            


            
            


               
            # **📌 Most Active Users (Overall)**
            if selected_user == "Overall":
                x, pie_data = active_user(df)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 🔥 Most Active Users")
                    
                    # Bar Chart
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color="skyblue")
                    ax.set_ylabel("Message Count")
                    # plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    st.markdown("### 🎯 User Contribution")
                    
                    # **Merge Small Users into 'Others'**
                    top_n = 5
                    top_users = pie_data.nlargest(top_n, "Count")
                    others_count = pie_data["Count"].sum() - top_users["Count"].sum()

                    new_pie_data = pd.concat([top_users, pd.DataFrame({"User": ["Others"], "Count": [others_count]})])

                    if new_pie_data.shape[0]==3:
                        new_pie_data=new_pie_data[new_pie_data["User"]!="Others"]

                    # Pie Chart
                    fig, ax = plt.subplots()
                    ax.pie(new_pie_data["Count"], labels=new_pie_data["User"], autopct="%1.1f%%", startangle=90)
                    st.pyplot(fig)
            


            # Emoji
            st.markdown("### Top Emojis Used")
            emoji_df=emojis(selected_user,df)

            cols=st.columns(len(emoji_df))

            for i,col in enumerate(cols):
                with col:
                    st.markdown(f"<h1 style='text-align:center';> {emoji_df['Emoji'][i]}</h1> ",unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center; font-size: 20px;'>{emoji_df['Count'][i]}</p>",unsafe_allow_html=True)

            # Word Cloud
            st.markdown("### ☁️ Word Cloud")
            df_wc=create_wordcloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Horizontal Bar graph
            
            Most_common_df=most_common_words(selected_user,df)
            st.markdown("### 💬 Most Common Words")
            fig, ax = plt.subplots()
            ax.barh(Most_common_df["Word"], Most_common_df["Count"], color="skyblue")
            ax.set_xlabel("Message Count")
            st.pyplot(fig)



            # Time line graph
            
            timeline_df=monthly_timeline(selected_user,df)
            st.markdown("### 💬 Monthly TimeLine")
            fig, ax = plt.subplots()
            ax.plot(timeline_df["Time"],timeline_df["Message"], color="skyblue")
            ax.set_ylabel("Message Count")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


            # plt.plot(timeline_df["Time"],timeline_df["Message"])
            # plt.xticks(rotation="vertical")
            

            # Daily TimeLine
            daily_df=daily_timeline(selected_user,df)
            st.markdown("### 💬 Daily TimeLine")
            fig, ax = plt.subplots()
            ax.plot(daily_df["Only Date"],daily_df["Message"], color="skyblue")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


            # Most active day
            days_df=most_active_day(selected_user,df)
            st.markdown("### 💬 Most Active Day")
            fig, ax = plt.subplots()
            ax.bar(days_df["Day Name"],days_df["count"])
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Most active Month
            month_df=most_active_month(selected_user,df)
            st.markdown("### 💬 Most Active Month")
            fig, ax = plt.subplots()
            ax.bar(month_df["Month"],month_df["count"])
            plt.xticks(rotation=45)
            st.pyplot(fig)



            


            

            

                        
    else:
        st.warning("⚠️ Please upload a `.txt` file.")
