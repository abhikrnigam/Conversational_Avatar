import logging
from audio_recorder import record_audio
from audio_transcriber import transcribe_audio
from chat_engine import ChatClient

logging.basicConfig(level=logging.DEBUG, filename="driver_logger.log")

logger = logging.getLogger(__name__)

def main():
    chat_client = ChatClient()
    logger.info("Recording....")
    print("Speak into the mic. Press CTRL+C to stop recording.")
    while True:
        try:
            # Step 1: Record
            audio_file = record_audio("abhishek_out.wav")
            logger.info("Recording completed")

            # Step 2: Transcribe
            print("Transcribing...")
            text = transcribe_audio(audio_file)
            print(f"You (transcribed): {text}")

            if text.strip().lower() == "quit":
                print("Chat closed")
                break

            # Step 3: Chat
            print("🤖 Bot:", end=" ")
            #response = chat_client.chat(text)
            #print(f"Response: {response}")

        except KeyboardInterrupt:
            print("Recording stopped by user, restarting loop...")
            continue  # go back to recording
if __name__ == "__main__":
    main()
