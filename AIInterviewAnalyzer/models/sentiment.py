from textblob import TextBlob


class SentimentAnalyzer:

    def analyze(self, text):

        analysis = TextBlob(text)

        polarity = analysis.sentiment.polarity

        if polarity > 0.2:
            sentiment = "Positive"

        elif polarity < -0.2:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 2)
        }