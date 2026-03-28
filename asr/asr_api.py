import os
import tempfile

import librosa
import torch
from fastapi import FastAPI, File, UploadFile
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

app = FastAPI()

# Task 2a: load model and processor once at startup
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
model.eval()


# Task 2b: ping endpoint to check if the service is running
@app.get("/ping")
def ping():
    return "pong"


# Task 2c: ASR endpoint — accepts an mp3 file and returns transcription + duration
@app.post("/asr")
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file to a temporary path
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Load audio, resample to 16kHz and convert to mono in one step
        waveform, _ = librosa.load(tmp_path, sr=16000, mono=True)

        # Calculate duration in seconds
        duration = round(len(waveform) / 16000, 1)

        # Run inference
        inputs = processor(
            waveform, sampling_rate=16000, return_tensors="pt", padding=True
        )
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        return {"transcription": transcription, "duration": str(duration)}

    finally:
        # Delete the uploaded file after processing
        os.remove(tmp_path)