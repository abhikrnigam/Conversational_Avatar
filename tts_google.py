def synthesize_text():
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    text = "Hello there. My name is Gapesh and I am a senior technical lead at google. I like eating fish with rice and water. I get very angry if i dont get mishti doi with my"
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voices = client.list_voices()
    print(voices)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Charon",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # The response's audio_content is binary.
    with open("output_gapesh.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output_gapesh.mp3"')

if __name__ == "__main__":
    synthesize_text()
