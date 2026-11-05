"""Offline contract tests using mocked responses, not live Watson scores."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import EMOTIONS, emotion_detector
from server import app


class TestOffline(unittest.TestCase):
    """Validate formatting, request construction, and error handling."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_formats_each_emotion(self, post):
        """Choose the maximum score for every possible dominant emotion."""
        for dominant in EMOTIONS:
            with self.subTest(dominant=dominant):
                scores = dict.fromkeys(EMOTIONS, 0.01)
                scores[dominant] = 0.96
                response = Mock(status_code=200)
                response.json.return_value = {
                    "emotionPredictions": [{"emotion": scores}]
                }
                post.return_value = response
                result = emotion_detector("A test sentence")
                self.assertEqual(result, {**scores, "dominant_emotion": dominant})
                self.assertEqual(
                    post.call_args.kwargs["json"],
                    {"raw_document": {"text": "A test sentence"}},
                )
                self.assertEqual(
                    post.call_args.kwargs["headers"]["grpc-metadata-mm-model-id"],
                    "emotion_aggregated-workflow_lang_en_stock",
                )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input(self, post):
        """Avoid calling Watson for blank text."""
        self.assertTrue(all(value is None for value in emotion_detector("  ").values()))
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request(self, post):
        """Represent HTTP 400 with empty emotion scores."""
        post.return_value = Mock(status_code=400)
        self.assertTrue(all(value is None for value in emotion_detector("?").values()))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_error(self, post):
        """Do not disguise an unavailable service as an emotion."""
        post.return_value = Mock(status_code=500)
        post.return_value.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            emotion_detector("Hello")

    def test_homepage(self):
        """Render the supplied template."""
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NLP - Emotion Detection", response.data)

    def test_blank_web_input(self):
        """Show the input validation message."""
        response = app.test_client().get("/emotionDetector?textToAnalyze=")
        self.assertIn(b"Invalid text!", response.data)

    @patch("server.emotion_detector")
    def test_web_result(self, detector):
        """Format every score and the dominant emotion."""
        detector.return_value = {
            **dict.fromkeys(EMOTIONS, 0.01), "anger": 0.96,
            "dominant_emotion": "anger",
        }
        response = app.test_client().get("/emotionDetector?textToAnalyze=I+am+angry")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"dominant emotion is anger", response.data)
        for emotion in EMOTIONS:
            self.assertIn(emotion.encode(), response.data)

    @patch("server.emotion_detector", side_effect=requests.ConnectionError())
    def test_web_outage(self, _detector):
        """Report a service outage with HTTP 503."""
        self.assertEqual(
            app.test_client().get("/emotionDetector?textToAnalyze=Hello").status_code,
            503,
        )


if __name__ == "__main__":
    unittest.main()
