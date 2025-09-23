# app.py
import logging
import gradio as gr

from vad_recorder import VADRecorder
from audio_transcriber import transcribe_audio
from chat_engine import ChatClient
from tts_engine_resemble import synthesize_and_play
from image_captioner import ImageCaptioner
from camera_capture import capture_image

logging.basicConfig(level=logging.DEBUG, filename="driver_logger.log")
logger = logging.getLogger(__name__)

# --- Singletons (kept alive across requests) ---
chat_client = ChatClient()
vad_recorder = VADRecorder(aggressiveness=2)
captioner = ImageCaptioner()  # OpenAI-based captioner (as you implemented)

def speak_and_chat():
    """
    Replicates one iteration of your driver loop:
    1) Record with VAD
    2) Transcribe
    3) If "capture image" in text -> capture + caption and append
    4) Chat with composed text
    5) TTS playback (server-side via your function)
    """
    # 1) VAD record
    audio_file = vad_recorder.record("user_input.wav")
    if not audio_file:
        return "No speech detected.", "", "", ""

    # 2) Transcribe
    user_text = transcribe_audio(audio_file) or ""
    if not user_text.strip():
        return "Could not transcribe speech.", "", "", ""

    # 3) Optional capture + caption
    caption = ""
    composed_input = user_text
    if "capture image" in user_text.lower():
        image_path = capture_image("captured.jpg")
        caption = captioner.caption_image(image_path)
        composed_input = (user_text.strip() + "\n\n" + f"[Image caption]: {caption}").strip()

    # 4) Chat
    bot_response = chat_client.chat(composed_input)

    # 5) TTS
    try:
        synthesize_and_play(bot_response)
        tts_status = "Played via server audio output."
    except Exception as e:
        tts_status = f"TTS error: {e}"

    return user_text, caption, bot_response, tts_status


def caption_uploaded_image(img):
    """
    Optional utility: caption any uploaded image from the Gradio UI.
    """
    if img is None:
        return "No image provided."
    # Gradio gives a PIL.Image; save then caption to reuse your code path
    tmp_path = "uploaded.jpg"
    img.save(tmp_path)
    return captioner.caption_image(tmp_path)


with gr.Blocks(title="Voice → (Capture?) → Caption → Chat") as demo:
    gr.Markdown("## 🎙️ Voice → 📸 (optional) → 📝 Caption → 🤖 Chat\n"
                "Say **'capture image'** during your voice input to take a photo and include its caption in the chat prompt.")

    with gr.Row():
        speak_btn = gr.Button("🎤 Speak (VAD) + Chat", variant="primary")
        # Optional: caption an uploaded image without voice
        img_in = gr.Image(label="(Optional) Upload image to caption", type="pil")
        caption_btn = gr.Button("🖼️ Caption Uploaded Image")

    with gr.Row():
        transcript_box = gr.Textbox(label="You (transcribed)", interactive=False)
        caption_box = gr.Textbox(label="Image Caption (if captured/uploaded)", interactive=False)

    bot_box = gr.Textbox(label="🤖 Bot Response", interactive=False, lines=4)
    tts_box = gr.Textbox(label="TTS Status", interactive=False)

    speak_btn.click(fn=speak_and_chat, inputs=None,
                    outputs=[transcript_box, caption_box, bot_box, tts_box])

    caption_btn.click(fn=caption_uploaded_image, inputs=[img_in], outputs=[caption_box])

if __name__ == "__main__":
    demo.launch()
