import pyaudio
import wave
import logging 
import whisper
logging.basicConfig(level=logging.DEBUG,filename='audio_processing.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def recordAudio():
    audio = pyaudio.PyAudio()
    logger.info("Recording audio..")
    stream = audio.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = 44100,
                        input = True,
                        frames_per_buffer = 1024)
    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        logger.info("Stopping audio recording!")
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    sound_file = wave.open("abhishek_out.wav","wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()


logger.info("Audio recording successful! ")

def transcriber():
    model = whisper.load_model("base")
    audio_file = "abhishek_out.mp3"
    result = model.transcribe(audio_file)
    print(result["text"])



if __name__ == "__main__":
    recordAudio()
    transcriber()