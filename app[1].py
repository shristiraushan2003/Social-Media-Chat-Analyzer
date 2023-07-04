import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer" )




uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    # st.dataframe(df)
    st.title(':red[Top statistics] :exploding_head:')
    # find unique users
    user_list=df['name'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total msg ")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total media")
            st.title(num_media)
        with col4:
            st.header("Total links")
            st.title(num_links)

    # message frequency:
        st.title(':red[Monthly Timeline] :hourglass_flowing_sand:')
        messages_df=helper.message_frequency(selected_user,df)
        
        col1, col2=st.columns(2)
        with col1:
            st.header('Message counts')
            st.dataframe(messages_df)
        with col2:
            st.header('Line Plot')
            st.line_chart(messages_df,x='time',y='message')
     
     # Daily time line frequency:
        st.title(':red[Daily Timeline] :hourglass_flowing_sand:')
        messages_df=helper.daily_timeline(selected_user,df)
        
        col1, col2=st.columns(2)
        with col1:
            st.header('Message counts')
            st.dataframe(messages_df)
        with col2:
            st.header('Line Plot')
            st.line_chart(messages_df,x='time',y='message')
    #  Activity map:
        st.title(':red[Activity Map] :hourglass_flowing_sand:')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month=helper.monthly_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.header("Activity heat map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

    # finding the busiest users in the group
        if selected_user =='Overall':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                 ax.bar(x.index,x.values)
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
 
# word cloud
        st.title(':red[Wordcloud] :snow_cloud:')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
# Most common Df
        st.title(':red[Most common words] :thinking_face:')
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# Analysis of emojies:
        st.title(':red[Most common Emojis] :face_with_head_bandage:')
        emoji_df=helper.most_common_emoji(selected_user,df)

        col1, col2=st.columns(2)

        with col1:
            st.header('Frequency of emojis')
            st.dataframe(emoji_df)
        with col2:
            st.header('Top 5 emojis')
            top_5_df = emoji_df.head(5)
            fig,ax=plt.subplots()
            ax.pie(top_5_df['frequency'], labels=top_5_df['emoji'], autopct='%1.1f%%')
            ax.axis('equal')
            st.pyplot(fig)


     


   
    