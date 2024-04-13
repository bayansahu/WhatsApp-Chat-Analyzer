from textblob import TextBlob

def sentiment(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    sentiments = []
    for message in df['message']:
        blob = TextBlob(str(message))
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            sentiment = 'Positive'
        elif sentiment_score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        sentiments.append(sentiment)

    # Add the sentiment column to the DataFrame
    df['sentiment'] = sentiments

    return df

def sentiment_analysis(df):

    # Count the occurrences of each sentiment
    num_messages = df.shape[0]
    positive_count = df['sentiment'].str.count('Positive').sum()
    positive_percentage = positive_count/num_messages * 100

    negative_count = df['sentiment'].str.count('Negative').sum()
    negative_percentage = negative_count / num_messages * 100

    neutral_count = df['sentiment'].str.count('Neutral').sum()
    neutral_percentage = neutral_count / num_messages * 100

    return positive_percentage,neutral_percentage,negative_percentage,positive_count,neutral_count,negative_count