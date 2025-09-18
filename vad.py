from faster_whisper import WhisperModel

model = WhisperModel("tiny.en") # or any other model size
segments, info = model.transcribe("sample_vad_abhishek.wav", vad_filter=True)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")