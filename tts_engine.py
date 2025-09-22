from google.cloud import texttospeech
from playsound import playsound
import logging

logger = logging.getLogger(__name__)

def synthesize_and_play(text, output_file="bot_response.mp3"):
    """Synthesizes speech from text using Google TTS and plays it."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Charon",  # You can change this voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # Save to file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        logger.info(f'Audio content written to file "{output_file}"')

    # Play the file
    playsound(output_file)
