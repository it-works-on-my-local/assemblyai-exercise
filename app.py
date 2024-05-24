import requests
import time
from textblob import TextBlob

# AssemblyAI API key and audio file URL
API_KEY = 'f7b91a0f92764e2db429300738fc13c1'
AUDIO_URL = 'https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3'
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

# Function to submit transcription request to AssemblyAI
def submit_transcription_request(audio_url):
    # Define request headers with API key
    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }
    try:
        # Send POST request to AssemblyAI endpoint with audio URL and request parameters
        response = requests.post(TRANSCRIPT_ENDPOINT, json={
            "audio_url": audio_url,
            "speaker_labels": True,
            "sentiment_analysis": True
        }, headers=headers)
        response.raise_for_status()
        # Extract and return the transcription ID from the response
        transcript_id = response.json()['id']
        print(f"Transcription ID: {transcript_id}")
        return transcript_id
    except requests.exceptions.RequestException as e:
        # Handle request errors and display error message
        print("An error occurred while submitting the transcription request:", e)
        exit(1)

# Function to check transcription status
def check_transcription_status(transcript_id):
    # Define request headers with API key
    headers = {
        "authorization": API_KEY
    }
    status = 'processing'
    # Poll the AssemblyAI endpoint until transcription is completed or failed
    while status not in ['completed', 'failed']:
        try:
            # Send GET request to AssemblyAI endpoint to check transcription status
            response = requests.get(f"{TRANSCRIPT_ENDPOINT}/{transcript_id}", headers=headers)
            response.raise_for_status()
            # Update transcription status from the response
            status = response.json()['status']
            print(f"Status: {status}")
            # Wait for 10 seconds before checking status again
            if status not in ['completed', 'failed']:
                time.sleep(10)
        except requests.exceptions.RequestException as e:
            # Handle request errors and display error message
            print("An error occurred while checking transcription status:", e)
            exit(1)
    return status

# Function to retrieve transcript data
def get_transcript_data(transcript_id):
    # Define request headers with API key
    headers = {
        "authorization": API_KEY
    }
    try:
        # Send GET request to AssemblyAI endpoint to retrieve transcript data
        response = requests.get(f"{TRANSCRIPT_ENDPOINT}/{transcript_id}", headers=headers)
        response.raise_for_status()
        # Return transcript data from the response
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request errors and display error message
        print("An error occurred while retrieving transcript data:", e)
        exit(1)

# Function to extract utterances from transcript data
def extract_utterances(transcript_data):
    utterances = {}
    # Iterate through each utterance in the transcript data
    for utterance in transcript_data.get('utterances', []):
        speaker = utterance.get('speaker')
        text = utterance.get('text')
        if speaker and text:
            # Add utterance text to the respective speaker's list
            utterances.setdefault(speaker, []).append(text)
    # Combine multiple utterances of each speaker into a single string
    return {speaker: ' '.join(texts) for speaker, texts in utterances.items()}

# Function to analyze sentiment of utterances
def analyze_sentiment(utterances):
    overall_sentiments = {}
    # Iterate through each speaker's utterances
    for speaker, text in utterances.items():
        # Perform sentiment analysis using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        # Determine sentiment based on polarity score
        if polarity > 0:
            overall_sentiments[speaker] = 'Positive'
        elif polarity < 0:
            overall_sentiments[speaker] = 'Negative'
        else:
            overall_sentiments[speaker] = 'Neutral'
    return overall_sentiments

# Function to calculate speaking time for each speaker
def calculate_speaking_time(utterances):
    total_duration = sum([len(text.split()) for text in utterances.values()])
    speaking_time = {}
    # Calculate speaking time percentage for each speaker
    for speaker, text in utterances.items():
        speaking_time[speaker] = (len(text.split()) / total_duration) * 100
    return speaking_time

# Function to print speaking time for each speaker
def print_speaking_time(speaking_time):
    print("\nSpeaking time for each speaker:")
    # Print speaking time percentage for each speaker in alphabetical order
    for speaker, time_percentage in sorted(speaking_time.items()):
        print(f"Speaker {speaker} spoke for {time_percentage:.2f}% of the time.")

# Function to print overall sentiment for each speaker
def print_overall_sentiment(overall_sentiments):
    print("\nOverall sentiment for each speaker:")
    # Print overall sentiment for each speaker in alphabetical order
    for speaker, sentiment in sorted(overall_sentiments.items()):
        print(f"The overall sentiment from Speaker {speaker} was {sentiment}.")

def main():
    # Submit transcription request and get the transcript ID
    transcript_id = submit_transcription_request(AUDIO_URL)
    
    # Check the transcription status
    status = check_transcription_status(transcript_id)
    
    # If transcription is completed, proceed with analysis
    if status == 'completed':
        # Retrieve transcript data from AssemblyAI API
        transcript_data = get_transcript_data(transcript_id)
        
        # Extract turn-by-turn utterances from transcript data
        utterances = extract_utterances(transcript_data)
        
        # Analyze sentiment of each utterance
        overall_sentiments = analyze_sentiment(utterances)
        
        # Calculate speaking time percentage for each speaker
        speaking_time = calculate_speaking_time(utterances)
        
        # Print the speaking time for each speaker
        print_speaking_time(speaking_time)
        
        # Print the overall sentiment for each speaker
        print_overall_sentiment(overall_sentiments)
    else:
        # If transcription failed, print an error message
        print("Transcription failed")

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
