# driver.py
from audio_recorder import record_audio
from audio_transcriber import transcribe_audio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='audio_transcription.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
driverLogger = logging.getLogger(__name__)


def main():
    print("Press CTRL+C to stop recording.")
    audio_file = record_audio("abhishek_out.wav")
    driverLogger.info("Audio transcription is process..")
    text = transcribe_audio(audio_file)
    driverLogger.info(f"transcription_result is: {text}")
    print("Transcription Result:")
    print(text)

if __name__ == "__main__":
    main()
