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
