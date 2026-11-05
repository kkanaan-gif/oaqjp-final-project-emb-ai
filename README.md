# Final Project

## Emotion Detector

A Flask web application that detects anger, disgust, fear, joy, and sadness
using the IBM Watson NLP service provided by Skills Network.

### Run in the Skills Network lab

```bash
cd /home/project/final_project
python3 -m pip install -r requirements.txt
python3 test_emotion_detection.py
python3 server.py
```

Open the lab preview for port 5000. The application uses the supplied HTML
interface and exposes `/emotionDetector?textToAnalyze=...`.

### Response format

The detector returns a dictionary with `anger`, `disgust`, `fear`, `joy`,
`sadness`, and `dominant_emotion`. Blank input returns None for every field.
Service outages are reported as HTTP 503 by the web endpoint.

### Tests and assignment evidence

- `test_emotion_detection.py`: five live Watson integration tests.
- `test_offline.py`: eight offline tests using explicitly mocked service responses.
- `collect_lab_evidence.sh`: runs the assignment commands in the actual lab
  and saves their command transcripts. Requires Watson service access.
- `evidence/`: code answers and local offline validation.

The Watson endpoint could not be reached from the development Mac. Offline
tests verify the application contract; they do not validate the model's emotion
predictions. The requested live transcripts under `/home/project/final_project`
must still be collected inside the Skills Network lab.
