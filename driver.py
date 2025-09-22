import logging
from audio_recorder import record_audio
from audio_transcriber import transcribe_audio
from chat_engine import ChatClient
from tts_engine import synthesize_and_play

logging.basicConfig(level=logging.DEBUG, filename="driver_logger.log")
logger = logging.getLogger(__name__)

def main():
    chat_client = ChatClient()
    logger.info("Recording started.")
    print("Speak into the mic. Press CTRL+C to stop recording.")

    while True:
        try:
            # Recording Audio
            audio_file = record_audio("abhishek_out.wav")
            logger.info("Recording completed")

            # Transcription
            print("Transcribing...")
            text = transcribe_audio(audio_file)
            print(f"You (transcribed): {text}")

            if text.strip().lower() == "quit":
                print("Chat closed")
                break

            # Response from chat engine
            print("🤖 Bot:", end=" ")
            response = chat_client.chat(text)
            print(f"Response: {response}")

            # Gcp TTS
            print("🔊 Playing bot response...")
            synthesize_and_play(response)

        except KeyboardInterrupt:
            print("Recording stopped by user, restarting loop...")
            continue

if __name__ == "__main__":
    main()
