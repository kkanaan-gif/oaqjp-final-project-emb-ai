"""Serve the Emotion Detector web interface and its analysis endpoint."""

from flask import Flask, render_template, request
from requests import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the supplied project interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Format the Watson scores for the browser."""
    text = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text)
    except (RequestException, KeyError, IndexError, TypeError, ValueError):
        return "Emotion service unavailable. Please try again later.", 503
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is 'anger': "
        f"{result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
