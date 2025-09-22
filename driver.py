import logging
from audio_recorder import record_audio
from vad_recorder import VADRecorder
from audio_transcriber import transcribe_audio
from chat_engine import ChatClient
from tts_engine_resemble import synthesize_and_play

logging.basicConfig(level=logging.DEBUG, filename="driver_logger.log")
logger = logging.getLogger(__name__)


def main():
    chat_client = ChatClient()
    vad_recorder = VADRecorder(aggressiveness=2)
    logger.info("Recording started.")
    print("Speak into the mic. Press CTRL+C to stop recording.")

    while True:
        try:
            # Step 1: VAD-based Recording
            audio_file = vad_recorder.record("user_input.wav")
            if not audio_file:
                print("⚠️ No speech detected, try again.")
                continue

            # Step 2: Transcribe
            print("Transcribing...")
            text = transcribe_audio(audio_file)
            print(f"You (transcribed): {text}")

            if text.strip().lower() == "quit":
                print("Chat closed")
                break

            # Step 3: Chat
            print("🤖 Bot:", end=" ")
            response = chat_client.chat(text)
            print(f"Response: {response}")

            # Step 4: TTS
            print("🔊 Playing bot response...")
            synthesize_and_play(response)

        except KeyboardInterrupt:
            print("Program stopped by user.")
            break


if __name__ == "__main__":
    main()
