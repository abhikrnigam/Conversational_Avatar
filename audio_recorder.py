# audio_recorder.py
import pyaudio
import wave
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='audio_recording.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def record_audio(output_file="abhishek_out.wav"):
    """
    Records audio until the user presses Ctrl+C.
    Returns the output file path.
    """
    audio = pyaudio.PyAudio()
    logger.info("Recording audio...")

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    frames = []
    print("🎤 Recording... (Press CTRL+C to stop)")

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        print("🛑 Recording stopped.")
        logger.info("Stopping audio recording...")

    # Cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_file, "wb") as sound_file:
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))

    logger.info(f"Audio saved to {output_file}")
    return output_file


def cleanup_audio():
    """No-op cleanup (kept for compatibility)."""
    pass
