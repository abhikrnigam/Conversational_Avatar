import collections
import pyaudio
import webrtcvad
import wave
import time

class VADRecorder:
    def __init__(self, aggressiveness=2, sample_rate=16000, frame_duration=30, silence_limit=3.0):
        """
        aggressiveness: 0-3, higher = more aggressive VAD
        sample_rate: must be 16000 for stable VAD
        frame_duration: frame size in ms (10, 20, or 30 only)
        silence_limit: seconds of silence before stopping recording
        """
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration
        self.frame_size = int(sample_rate * frame_duration / 1000)  # samples per frame
        self.silence_limit = silence_limit

        self.audio_interface = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        if self.stream is None:
            self.stream = self.audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.frame_size
            )

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def record(self, output_path="output.wav"):
        self.start_stream()
        print("🎙️ Speak now... (Recording will stop after silence)")

        frames = []
        silence_start = None

        while True:
            frame = self.stream.read(self.frame_size, exception_on_overflow=False)
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if is_speech:
                frames.append(frame)
                silence_start = None  # reset silence timer
            else:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > self.silence_limit:
                    print("⏹️ Stopped recording (silence detected)")
                    break

        self.stop_stream()

        # Save audio
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio_interface.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames))

        return output_path
