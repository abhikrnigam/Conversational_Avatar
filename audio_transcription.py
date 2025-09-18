import whisper


model = whisper.load_model("tiny.en")

# Apni .wav file ka path yahan dein
audio_file_path = "apni_audio_file.w"

try:
    # Model ko audio file par chalayein
    print(f"'{audio_file_path}' file ko transcribe kar rahe hain...")
    result = model.transcribe(audio_file_path, fp16=False) # fp16=False GPU ke bina bhi chalne deta hai

    # Transcribe kiya hua text print karein
    print("\n--- Transcription Result ---")
    print(result["text"])
    print("----------------------------")

except FileNotFoundError:
    print(f"Error: '{audio_file_path}' file nahi mili. Kripya sahi path dein.")
except Exception as e:
    print(f"Ek error aa gayi: {e}")