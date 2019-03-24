from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Returns a dict with the keys neg, neu, pos and compound
def assess(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment
