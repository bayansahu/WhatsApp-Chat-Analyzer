import streamlit as st
from preprocessor import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from sentiment import sentiment , sentiment_analysis
from language import language_detection
import pdfkit

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Sentiment Analysis
        s_df = sentiment(selected_user,df)
        positive_per, neutral_per, negative_per, pos, neu, neg = sentiment_analysis(s_df)

        st.title("Sentiment Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Positive Message")
            st.title(pos)

        with col2:
            st.header("Neutral Message")
            st.title(neu)

        with col3:
            st.header("Negative Message")
            st.title(neg)

        sen = [positive_per, neutral_per, negative_per]
        labels = ['Positive', 'Neutral', 'Negative']
        fig, ax = plt.subplots()
        ax.pie(sen, labels=labels, autopct="%0.2f")
        st.pyplot(fig)

        num_messages, words, num_media_messages, links= helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        #language Detector
        ldf = language_detection(df)
        st.dataframe(ldf)

        # Button to download DataFrame and Pie Chart as PDF
        if st.button("Download PDFs"):
            # Save the DataFrame as HTML table
            df_html = emoji_df.to_html()

            # Save the Pie Chart as PNG
            fig.savefig('pie_chart.png')

            # Convert HTML table and PNG to PDF using pdfkit
            pdfkit_options = {
                'page-size': 'A4',
                'dpi': 400,
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
            }

            pdfkit.from_string(df_html, 'emoji_analysis.pdf', options=pdfkit_options)
            pdfkit.from_file('pie_chart.png', 'pie_chart.pdf', options=pdfkit_options)

            # Provide a download button for the generated PDFs
            with open('emoji_analysis.pdf', 'rb') as f1, open('pie_chart.pdf', 'rb') as f2:
                emoji_pdf_bytes = f1.read()
                pie_chart_pdf_bytes = f2.read()
                st.download_button(label='Download Emoji Analysis PDF', data=emoji_pdf_bytes, file_name='emoji_analysis.pdf', mime='application/pdf')
                st.download_button(label='Download Pie Chart PDF', data=pie_chart_pdf_bytes, file_name='pie_chart.pdf',mime='application/pdf')

