import pandas as pd
from langdetect import detect_langs

def language_detection(df):
    # Create an empty dictionary to store language counts
    lang_count = {}

    # Iterate over each message in the DataFrame
    for message in df['message']:
        try:
            # Detect the language of the message and get the language code
            lang = detect_langs(message)[0].lang
            # Increment the count for the detected language
            lang_count[lang] = lang_count.get(lang, 0) + 1
        except Exception as e:
            # If language detection fails, skip the message and print the error
            print(f"Error detecting language: {e}")
            continue

    # Calculate the total number of messages
    total_messages = len(df)

    # Calculate the percentage of each language
    lang_percentage = {lang: count / total_messages * 100 for lang, count in lang_count.items()}

    # Create a DataFrame from the language percentages
    lang_df = pd.DataFrame(lang_percentage.items(), columns=['Language', 'Percentage'])

    return lang_df