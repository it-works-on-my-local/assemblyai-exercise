import requests
import time

def submit_transcription_request(audio_url, api_key):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    try:
        response = requests.post(transcript_endpoint, json={
            "audio_url": audio_url,
            "speaker_labels": True,
            "sentiment_analysis": True
        }, headers=headers)
        response.raise_for_status()  # Raise an exception if the request fails
        return response.json()['id']
    except requests.exceptions.RequestException as e:
        print("An error occurred while submitting the transcription request:", e)
        return None

def wait_for_transcription(transcript_id, api_key):
    transcript_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }

    status = 'processing'
    while status not in ['completed', 'failed']:
        try:
            response = requests.get(transcript_endpoint, headers=headers)
            response.raise_for_status()  # Raise an exception if the request fails
            status = response.json()['status']
            print(f"Status: {status}")
            if status not in ['completed', 'failed']:
                time.sleep(10)
        except requests.exceptions.RequestException as e:
            print("An error occurred while checking transcription status:", e)
            return None

    return status

def extract_utterances(transcript_data):
    utterances = transcript_data.get('utterances', [])
    if not utterances:
        print("No utterances found in the transcription data.")
        return []

    return utterances

def write_utterances_to_file(utterances):
    try:
        with open('utterances.txt', 'w') as f:
            for utterance in utterances:
                speaker = utterance.get('speaker')
                text = utterance.get('text')
                if speaker and text:
                    f.write(f"Speaker {speaker}: \"{text}\"\n\n")
    except IOError as e:
        print("An error occurred while writing utterances to file:", e)

def calculate_speaking_time(utterances):
    total_duration = sum([u['end'] - u['start'] for u in utterances])
    speaking_time = {}
    for utterance in utterances:
        speaker = utterance['speaker']
        duration = utterance['end'] - utterance['start']
        speaking_time[speaker] = speaking_time.get(speaker, 0) + duration

    return {speaker: (duration / total_duration) * 100 for speaker, duration in speaking_time.items()}

def determine_overall_sentiment(utterances):
    sentiments = {}
    for utterance in utterances:
        speaker = utterance.get('speaker')
        sentiment = utterance.get('sentiment')
        if speaker and sentiment:
            if speaker in sentiments:
                sentiments[speaker].append(sentiment)
            else:
                sentiments[speaker] = [sentiment]

    return {speaker: max(sentiments[speaker], key=sentiments[speaker].count) for speaker in sentiments}

def main():
    API_KEY = 'f7b91a0f92764e2db429300738fc13c1'
    AUDIO_URL = 'https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3'

    # Submit transcription request
    transcript_id = submit_transcription_request(AUDIO_URL, API_KEY)
    if not transcript_id:
        exit(1)

    print(f"Transcription ID: {transcript_id}")

    # Wait for transcription to complete
    status = wait_for_transcription(transcript_id, API_KEY)
    if status != 'completed':
        print("Transcription failed")
        exit(1)

    # Retrieve transcription data
    transcript_data = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers={"authorization": API_KEY}).json()

    # Extract utterances and write to file
    utterances = extract_utterances(transcript_data)
    write_utterances_to_file(utterances)

    # Calculate speaking time for each speaker
    speaking_time = calculate_speaking_time(utterances)
    print("Speaking time for each speaker:")
    for speaker, percentage in sorted(speaking_time.items()):
        print(f"Speaker {speaker} spoke for {percentage:.2f}% of the time.")

    # Determine overall sentiment for each speaker
    sentiments = determine_overall_sentiment(utterances)
    print("\nOverall sentiment for each speaker:")
    for speaker, sentiment in sorted(sentiments.items()):
        print(f"The overall sentiment for Speaker {speaker} was {sentiment}.")

if __name__ == "__main__":
    main()
