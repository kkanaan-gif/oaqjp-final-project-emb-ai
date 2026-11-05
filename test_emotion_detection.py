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
