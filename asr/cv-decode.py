# Task 2d: Batch decode script for Common Voice dataset. 

import os
import pandas as pd
import requests

ASR_URL = "http://localhost:8001/asr"
CSV_PATH = "cv-valid-dev/cv-valid-dev.csv"
AUDIO_DIR = "cv-valid-dev"

def transcribe(filepath: str) -> str:
    """Send an mp3 file to the ASR API and return the transcription."""
    with open(filepath, "rb") as f:
        response = requests.post(ASR_URL, files={"file": (os.path.basename(filepath), f, "audio/mpeg")})
    response.raise_for_status()
    return response.json()["transcription"]


def main():
    df = pd.read_csv(CSV_PATH)
    if "generated_text" not in df.columns:
        df["generated_text"] = ""

    total = len(df)
    for i, row in df.iterrows():
        filepath = row["filename"]

        if not os.path.exists(filepath):
            print(f"[{i+1}/{total}] MISSING: {filepath}")
            df.at[i, "generated_text"] = ""
            continue

        try:
            text = transcribe(filepath)
            df.at[i, "generated_text"] = text
            print(f"[{i+1}/{total}] {row['filename']} -> {text}")
        except Exception as e:
            print(f"[{i+1}/{total}] ERROR: {row['filename']} — {e}")
            df.at[i, "generated_text"] = ""

    df.to_csv(CSV_PATH, index=False)
    print(f"\nDone. Saved to {CSV_PATH}")


if __name__ == "__main__":
    main()