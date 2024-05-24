import requests
import time
from collections import Counter

API_KEY = 'f7b91a0f92764e2db429300738fc13c1'
AUDIO_URL = 'https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3'

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

# Submit transcription request
try:
    response = requests.post(transcript_endpoint, json={
        "audio_url": AUDIO_URL,
        "speaker_labels": True,
        "sentiment_analysis": True
    }, headers=headers)
    response.raise_for_status()  # Raise an exception if the request fails
    transcript_id = response.json()['id']
    print(f"Transcription ID: {transcript_id}")
except requests.exceptions.RequestException as e:
    print("An error occurred while submitting the transcription request:", e)
    exit(1)

# Wait for transcription to complete
status = 'processing'
while status not in ['completed', 'failed']:
    try:
        response = requests.get(f"{transcript_endpoint}/{transcript_id}", headers=headers)
        response.raise_for_status()  # Raise an exception if the request fails
        status = response.json()['status']
        print(f"Status: {status}")
        if status not in ['completed', 'failed']:
            time.sleep(10)
    except requests.exceptions.RequestException as e:
        print("An error occurred while checking transcription status:", e)
        exit(1)

# Check if transcription completed successfully
if status == 'failed':
    print("Transcription failed")
    exit()

transcript_data = response.json()

# Extract utterances and calculate sentiment for each speaker
utterances = transcript_data.get('utterances', [])
if not utterances:
    print("No utterances found in the transcription data.")
else:
    speaker_sentiments = {}
    for utterance in utterances:
        speaker = utterance.get('speaker')
        sentiment = utterance.get('sentiment')
        if speaker and sentiment:
            if speaker not in speaker_sentiments:
                speaker_sentiments[speaker] = []
            speaker_sentiments[speaker].append(sentiment)

    if not speaker_sentiments:
        print("No sentiment data found.")
    else:
        for speaker, sentiments in speaker_sentiments.items():
            sentiment_counts = Counter(sentiments)
            max_count = max(sentiment_counts.values())
            common_sentiments = [s for s, count in sentiment_counts.items() if count == max_count]
            sentiment_output = " and ".join(common_sentiments)
            print(f"The overall sentiment from Speaker {speaker} was {sentiment_output}.")
