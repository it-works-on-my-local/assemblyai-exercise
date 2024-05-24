# AssemblyAI Transcription and Analysis

This project utilizes the AssemblyAI API to transcribe an audio file, perform speaker diarization, and sentiment analysis.

## Setup

1. Clone the repository:
    ```bash
    gh repo clone it-works-on-my-local/assemblyai-exercise
    ```

2. Navigate to the project directory:
    ```bash
    cd assemblyai-excercise
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```bash
    python app.py
    ```

2. Monitor the terminal for the transcription status and analysis results.

## Functionality

### 1. Transcription

The script submits a transcription request to the AssemblyAI API using the provided audio URL. Speaker labels and sentiment analysis features are included in the request.

### 2. Speaker Diarization

After the transcription is completed, the script extracts turn-by-turn speaker diarization from the transcript data.

### 3. Speaking Time Calculation

The script calculates the percentage of speaking time for each speaker in the audio file and prints the results to the terminal.

### 4. Sentiment Analysis

The script determines the overall sentiment for each speaker in the audio file and prints the results to the terminal.

## Error Handling

The script includes error handling to manage exceptions during the transcription process or API requests. Error messages are displayed to the user with relevant information to diagnose and resolve issues.


## Improvements

- **Need more test cases**: Basic test cases only, need flows like happy flow and sad flow cases to cover.
- **Enhanced Error Handling**: Implement more robust error handling to cover additional edge cases and provide better user feedback.
- **Add Logging**: Utilize logging to record essential events and information during execution. Log messages are written to a log file, ensuring a detailed history of actions performed and any encountered errors.
- **Optimized API Usage**: Explore ways to optimize API usage, such as batching requests or implementing retry mechanisms for failed requests.
- **User Interface**: Develop a user interface for easier interaction with the transcription and analysis features.
- **Customization Options**: Add options for customizing transcription settings, such as language detection or audio quality adjustments.
- **Scalability**: Investigate strategies for scaling the application to handle larger audio files or higher volumes of requests.

## Considerations for Edge Cases

- **Incomplete Transcriptions**: Handle cases where the transcription process fails to complete or only partially completes due to issues with the audio file or network connectivity.
- **Speaker Identification Errors**: Address situations where the speaker identification algorithm incorrectly assigns utterances to speakers, leading to inaccuracies in speaker diarization and sentiment analysis.
- **API Rate Limiting**: Account for API rate limits and implement appropriate strategies, such as rate limiting and backoff mechanisms, to prevent exceeding usage limits and avoid service interruptions.
- **Unsupported Audio Formats**: Handle cases where the audio file format is not supported by the AssemblyAI API, ensuring graceful handling of unsupported formats and providing informative error messages to users.
- **Long Processing Times**: Mitigate long processing times for large audio files by implementing optimizations such as asynchronous processing or chunking the audio file into smaller segments.


## Common Errors and Troubleshooting

### 1. Transcription Request Errors

- **Error:** An error occurred while submitting the transcription request.
  - **Possible Causes:** This error may occur due to various reasons, including:
    - Network connectivity issues preventing communication with the AssemblyAI API.
    - Invalid API key provided in the configuration.
    - Incorrect audio URL format or accessibility issues.
  - **Troubleshooting Steps:**
    - Double-check the network connection and ensure that the system can access external APIs.
    - Verify the correctness of the API key provided in the script.
    - Ensure that the audio URL is accessible and points to a valid audio file.

### 2. Transcription Status Check Errors

- **Error:** An error occurred while checking transcription status.
  - **Possible Causes:** This error can occur if there are issues with the AssemblyAI API response or network connectivity problems during the status check process.
  - **Troubleshooting Steps:**
    - Check the network connection to ensure it's stable and capable of reaching external APIs.
    - Retry the status check after a short delay in case of temporary network issues.

### 3. Transcript Data Retrieval Errors

- **Error:** An error occurred while retrieving transcript data.
  - **Possible Causes:** This error may occur if the AssemblyAI API fails to provide the transcript data due to internal server errors, invalid transcript IDs, or network issues.
  - **Troubleshooting Steps:**
    - Verify the correctness of the transcript ID used for data retrieval.
    - Check the network connection and retry the data retrieval process.

### General Troubleshooting Tips

- Ensure that the provided audio file URL is accessible and points to the correct file.
- Double-check the API key used for authentication with the AssemblyAI API.
- Review the error messages carefully to identify potential causes and follow the troubleshooting steps provided.

## Sample Output
    ```bash
    Transcription ID: 31a9b26a-05d9-4c03-b95c-3847cca04cc6
    Status: processing
    Status: processing
    Status: completed

    Speaking time for each speaker:
    Speaker A spoke for 34.29% of the time.
    Speaker B spoke for 65.71% of the time.

    Overall sentiment for each speaker:
    The overall sentiment from Speaker A was Positive.
    The overall sentiment from Speaker B was Positive. 
    ```