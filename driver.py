# driver.py
import logging
from vad_recorder import VADRecorder
from audio_transcriber import transcribe_audio
from chat_engine import ChatClient
from tts_engine_resemble import synthesize_and_play
from image_captioner import ImageCaptioner
from camera_capture import capture_image

logging.basicConfig(level=logging.DEBUG, filename="driver_logger.log")
logger = logging.getLogger(__name__)

def main():
    chat_client = ChatClient()
    vad_recorder = VADRecorder(aggressiveness=2)
    captioner = ImageCaptioner()  # OpenAI-based captioner

    logger.info("Recording started.")
    print("Speak into the mic. Say 'capture image' to take a photo. Type CTRL+C to stop.")

    while True:
        try:
            # 1) Record user speech
            audio_file = vad_recorder.record("user_input.wav")
            if not audio_file:
                print("⚠️ No speech detected, try again.")
                continue

            # 2) Transcribe
            print("Transcribing...")
            user_text = transcribe_audio(audio_file) or ""
            print(f"You (transcribed): {user_text}")

            if user_text.strip().lower() == "quit":
                print("Chat closed")
                break

            # 3) Optional: capture + caption
            composed_input = user_text
            if "capture image" in user_text.lower():
                image_path = capture_image("captured.jpg")
                print("🖼️ Generating caption for captured image...")
                caption = captioner.caption_image(image_path)
                print(f"[Image caption]: {caption}")

                # Pass BOTH the user text and the image caption to the chat engine
                # (keeps your existing chat flow intact, just richer context)
                composed_input = (user_text.strip() + "\n\n"
                                  f"[Image caption]: {caption}").strip()

            # 4) Chat
            print("🤖 Bot:", end=" ")
            response = chat_client.chat(composed_input)
            print(f"Response: {response}")

            # 5) TTS
            print("🔊 Playing bot response...")
            synthesize_and_play(response)

        except KeyboardInterrupt:
            print("Program stopped by user.")
            break

if __name__ == "__main__":
    main()
