def sentiment_desc(sentiment_value):
    if -1 <= sentiment_value < -0.05:
        return "Possible scam warning"
    elif -0.05 <= sentiment_value <= 0.05:
        return "Unbiased discussion"
    elif 0.05 < sentiment_value <= 1:
        return "Possible hype promotion"
    else:
        return "Invalid score"  # Edge case handling