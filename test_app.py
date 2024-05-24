import unittest
from unittest.mock import patch
from app import (
    submit_transcription_request,
    check_transcription_status,
    get_transcript_data,
    extract_utterances,
    analyze_sentiment,
    calculate_speaking_time,
)

class TestAppFunctions(unittest.TestCase):
    
    @patch('app.requests.post')
    def test_submit_transcription_request(self, mock_post):
        mock_response = {'id': 'transcript_id'}
        mock_post.return_value.json.return_value = mock_response
        transcript_id = submit_transcription_request('test_audio_url')
        self.assertEqual(transcript_id, 'transcript_id')

    @patch('app.requests.get')
    def test_check_transcription_status(self, mock_get):
        # Test case for completed transcription
        mock_response_completed = {'status': 'completed'}
        mock_get.return_value.json.return_value = mock_response_completed
        status_completed = check_transcription_status('test_transcript_id_completed')
        self.assertEqual(status_completed, 'completed')

        # Test case for failed transcription
        mock_response_failed = {'status': 'failed'}
        mock_get.return_value.json.return_value = mock_response_failed
        status_failed = check_transcription_status('test_transcript_id_failed')
        self.assertEqual(status_failed, 'failed')

    @patch('app.requests.get')
    def test_get_transcript_data(self, mock_get):
        # Test case for successful retrieval of transcript data
        mock_response = {'transcript': 'test_transcript'}
        mock_get.return_value.json.return_value = mock_response
        transcript_data = get_transcript_data('test_transcript_id')
        self.assertEqual(transcript_data, {'transcript': 'test_transcript'})

        # Test case for missing transcript data
        mock_get.return_value.json.return_value = {}
        transcript_data_missing = get_transcript_data('test_transcript_id_missing')
        self.assertEqual(transcript_data_missing, {})

    def test_extract_utterances(self):
        # Test case with valid transcript data
        transcript_data = {
            'utterances': [
                {'speaker': 'A', 'text': 'Hello'},
                {'speaker': 'B', 'text': 'Hi there'},
            ]
        }
        utterances = extract_utterances(transcript_data)
        self.assertEqual(utterances, {'A': 'Hello', 'B': 'Hi there'})

        # Test case with empty transcript data
        transcript_data_empty = {}
        utterances_empty = extract_utterances(transcript_data_empty)
        self.assertEqual(utterances_empty, {})

    def test_analyze_sentiment(self):
        # Test case with neutral sentiment for both speakers
        utterances_neutral = {'A': 'Maybe', 'B': 'Cannot say'}
        sentiments_neutral = analyze_sentiment(utterances_neutral)
        self.assertEqual(sentiments_neutral, {'A': 'Neutral', 'B': 'Neutral'})

    def test_calculate_speaking_time(self):
        # Test case with equal speaking time
        utterances_equal = {'A': 'Hello, how are you?', 'B': 'Hi there, I do use whatsapp!'}
        speaking_time_equal = calculate_speaking_time(utterances_equal)
        self.assertAlmostEqual(speaking_time_equal['A'], 40.0, delta=0.01)
        self.assertAlmostEqual(speaking_time_equal['B'], 60.0, delta=0.01)

        # Test case with one speaker speaking for the entire duration
        utterances_single = {'A': 'Hello, how are you?'}
        speaking_time_single = calculate_speaking_time(utterances_single)
        self.assertAlmostEqual(speaking_time_single['A'], 100.0, delta=0.01)

        # Test case with no spoken text
        utterances_empty = {}
        speaking_time_empty = calculate_speaking_time(utterances_empty)
        self.assertEqual(speaking_time_empty, {})

if __name__ == '__main__':
    unittest.main()
