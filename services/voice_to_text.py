import requests
from core.config import settings

#ASSEMBLYAI_API_KEY = settings.ASSEMBLYAI_API_KEY
ASSEMBLYAI_API_KEY = ""
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": ASSEMBLYAI_API_KEY,
    "content-type": "application/json"
}

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Upload audio bytes to AssemblyAI and get transcription text.
    """

    # Step 1: Upload audio
    upload_response = requests.post(
        UPLOAD_ENDPOINT,
        headers={"authorization": ASSEMBLYAI_API_KEY},
        data=audio_bytes
    )
    upload_response.raise_for_status()
    upload_url = upload_response.json()['upload_url']

    # Step 2: Request transcription
    transcript_request = {
        "audio_url": upload_url,
        "language_code": "en"  # or "fa" for Persian if supported
    }
    transcript_response = requests.post(
        TRANSCRIPT_ENDPOINT,
        json=transcript_request,
        headers=headers
    )
    transcript_response.raise_for_status()
    transcript_id = transcript_response.json()['id']

    # Step 3: Poll until completed
    import time
    while True:
        polling_response = requests.get(
            f"{TRANSCRIPT_ENDPOINT}/{transcript_id}",
            headers=headers
        )
        polling_response.raise_for_status()
        status = polling_response.json()['status']
        if status == 'completed':
            return polling_response.json().get('text', '')
        elif status == 'error':
            raise Exception("Transcription failed: " + polling_response.json().get('error', 'Unknown error'))
        else:
            time.sleep(2)
