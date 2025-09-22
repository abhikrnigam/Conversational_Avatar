import os
from resemble import Resemble
import requests
import time
from dotenv import load_dotenv

load_dotenv()


Resemble.api_key(os.get_env("RESEMBLE_API_KEY"))

# Get your default Resemble project.
project_uuid = os.getenv("RESEMBLE_PROJECT_UUID")

# Get your Voice uuid. In this example, we'll obtain the first.
voice_uuid = os.get_env("RESEMBLE_VOICE_UUID")

# Let's create a clip!
body = input()
start_time = time.time()
response = Resemble.v2.clips.create_sync(project_uuid,
                                         voice_uuid,
                                         body,
                                         title=None,
                                         sample_rate=None,
                                         output_format=None,
                                         precision=None,
                                         include_timestamps=None,
                                         is_archived=None,
                                         raw=None)
audio_url = response['item']['audio_src']
print(audio_url)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")

requesturl = requests.get(audio_url)
op = "/home/megha/Desktop/output.wav"
with open(op, "wb") as f:
	f.write(requesturl.content)
#print(clip['audio_src'])
