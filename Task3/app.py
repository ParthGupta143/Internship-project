from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)


def get_sentiment_label(polarity: float) -> str:
    """
    Polarity range: -1 (very negative) to +1 (very positive)
    Threshold:
      - |polarity| < 0.05  => Neutral
      - polarity >= 0.05   => Positive
      - polarity <= -0.05  => Negative
    """
    if polarity >= 0.05:
        return "Positive"
    elif polarity <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def get_sentiment_emoji(polarity: float) -> str:
    """Return an emoji according to sentiment strength."""
    if polarity >= 0.6:
        return "😄"   # strongly positive
    elif polarity >= 0.2:
        return "🙂"   # mildly positive
    elif polarity <= -0.6:
        return "😡"   # strongly negative
    elif polarity <= -0.2:
        return "🙁"   # mildly negative
    else:
        return "😐"   # neutral


def get_intensity_label(polarity: float) -> str:
    """More detailed description like 'Strongly Positive' etc."""
    if -0.05 < polarity < 0.05:
        return "Neutral"

    direction = "Positive" if polarity > 0 else "Negative"
    strength = abs(polarity)

    if strength < 0.2:
        prefix = "Slightly"
    elif strength < 0.5:
        prefix = "Moderately"
    else:
        prefix = "Strongly"

    return f"{prefix} {direction}"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_text = request.form.get("user_text", "").strip()

        if user_text:
            blob = TextBlob(user_text)
            polarity = round(blob.sentiment.polarity, 3)
            subjectivity = round(blob.sentiment.subjectivity, 3)

            label = get_sentiment_label(polarity)
            emoji = get_sentiment_emoji(polarity)
            intensity = get_intensity_label(polarity)

            # extra stats
            words = len(user_text.split())
            chars_no_space = len(user_text.replace(" ", ""))

            result = {
                "text": user_text,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "label": label,
                "emoji": emoji,
                "intensity": intensity,
                "word_count": words,
                "char_count": chars_no_space,
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    # Debug mode for development
    app.run(debug=True)
