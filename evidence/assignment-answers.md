# Final answers — all 16 questions

Live Watson outputs were generated in the Skills Network lab. Copy code and terminal text into text questions; paste URLs only for Questions 1 and 6. Upload the PNG files for Questions 11 and 14.

## Question 1

https://github.com/kkanaan-gif/oaqjp-final-project-emb-ai/blob/main/README.md

## Question 2

Paste this code:

```python
"""Initial Watson NLP application returning the raw service response."""

import requests


def emotion_detector(text_to_analyze):
    """Send text to Watson EmotionPredict and return its response text."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id":
            "emotion_aggregated-workflow_lang_en_stock"
    }
    response = requests.post(
        url,
        headers=headers,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    response.raise_for_status()
    return response.text
```

## Question 3

Paste this actual terminal transcript:

```text
/home/project/final_project $ python3
from emotion_detection import emotion_detector
print(emotion_detector('I am really mad about this'))
exit()
Python 3.10.12 (main, Aug 31 2026, 10:18:17) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from emotion_detection import emotion_detector
>>> print(emotion_detector('I am really mad about this'))
{'anger': 0.6674731, 'disgust': 0.022848725, 'fear': 0.09749009, 'joy': 0.011863918, 'sadness': 0.1953058, 'dominant_emotion': 'anger'}
>>> exit()
/home/project/final_project $ python3 test_emotion_detection.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.630s

OK
```

## Question 4

Paste this code:

```python
"""Detect emotions with the Watson NLP service supplied by Skills Network."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the highest-scoring emotion.

    Blank input or a service rejection (HTTP 400) returns None for all
    fields. Connection errors and other HTTP errors propagate to the caller.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not text_to_analyze or not text_to_analyze.strip():
        return empty_result
    response = requests.post(
        URL,
        headers=HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    emotion = response.json()["emotionPredictions"][0]["emotion"]
    result = {name: emotion[name] for name in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
```

## Question 5

Paste this actual terminal transcript:

```text
/home/project/final_project $ python3 -c 'from emotion_detection import emotion_detector; print(emotion_detector('"'"'I am really mad about this'"'"'))'
{'anger': 0.6674731, 'disgust': 0.022848725, 'fear': 0.09749009, 'joy': 0.011863918, 'sadness': 0.1953058, 'dominant_emotion': 'anger'}
```

## Question 6

https://github.com/kkanaan-gif/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py

## Question 7

Paste this actual terminal transcript:

```text
/home/project/final_project $ python3 -c 'from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('"'"'I am very angry'"'"'))'
{'anger': 0.97299534, 'disgust': 0.007920562, 'fear': 0.021403823, 'joy': 0.0111511685, 'sadness': 0.047718644, 'dominant_emotion': 'anger'}
```

## Question 8

Paste this code:

```python
"""Live Watson NLP tests; run inside the Skills Network lab."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Check the dominant emotion for the five required example sentences."""

    def check_emotion(self, text, expected):
        """Check the complete response and its dominant emotion."""
        result = emotion_detector(text)
        self.assertEqual(
            set(result),
            {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"},
        )
        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self):
        """Recognize joy."""
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Recognize anger."""
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Recognize disgust."""
        self.check_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Recognize sadness."""
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Recognize fear."""
        self.check_emotion("I am really afraid that this will happen", "fear")


if __name__ == "__main__":
    unittest.main()
```

## Question 9

Paste this actual terminal transcript:

```text
/home/project/final_project $ python3 test_emotion_detection.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.594s

OK
```

## Question 10

Paste this code:

```python
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
```

## Question 11

Upload [6b_deployment_test.png](6b_deployment_test.png).

## Question 12

Paste this code:

```python
"""Detect emotions with the Watson NLP service supplied by Skills Network."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the highest-scoring emotion.

    Blank input or a service rejection (HTTP 400) returns None for all
    fields. Connection errors and other HTTP errors propagate to the caller.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not text_to_analyze or not text_to_analyze.strip():
        return empty_result
    response = requests.post(
        URL,
        headers=HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    emotion = response.json()["emotionPredictions"][0]["emotion"]
    result = {name: emotion[name] for name in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
```

## Question 13

Paste this code:

```python
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
```

## Question 14

Upload [7c_error_handling_interface.png](7c_error_handling_interface.png).

## Question 15

Paste this code:

```python
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
```

## Question 16

Paste this actual terminal transcript:

```text
$ pylint --persistent=n server.py

------------------------------------
Your code has been rated at 10.00/10

```
