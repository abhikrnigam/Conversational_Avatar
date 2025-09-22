import os
import time
import requests
import logging
from dotenv import load_dotenv
from resemble import Resemble
from playsound import playsound

# Load API keys from .env
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Resemble API
Resemble.api_key(os.getenv("RESEMBLE_API_KEY"))

PROJECT_UUID = os.getenv("RESEMBLE_PROJECT_UUID")
VOICE_UUID = os.getenv("RESEMBLE_VOICE_UUID")


def synthesize_and_play(text, output_file="bot_response.wav"):
    """
    Synthesizes speech using Resemble AI and plays it.
    """
    if not PROJECT_UUID or not VOICE_UUID:
        raise ValueError("Missing PROJECT_UUID or VOICE_UUID in environment variables")

    logger.info("Starting TTS synthesis with Resemble...")

    start_time = time.time()

    # Create clip synchronously
    response = Resemble.v2.clips.create_sync(
        PROJECT_UUID,
        VOICE_UUID,
        text,
        title=None,
        sample_rate=None,
        output_format="wav",  # ensure wav for playsound compatibility
        precision=None,
        include_timestamps=None,
        is_archived=None,
        raw=None,
    )

    audio_url = response["item"]["audio_src"]
    logger.debug(f"Audio URL: {audio_url}")

    # Download the audio
    request_url = requests.get(audio_url)
    with open(output_file, "wb") as f:
        f.write(request_url.content)

    elapsed_time = time.time() - start_time
    logger.info(f"TTS completed in {elapsed_time:.2f} seconds. Audio saved at {output_file}")

    # Play the audio
    playsound(output_file)
