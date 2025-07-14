import tkinter as tk
from tkinter import filedialog, scrolledtext
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    # Convert m4a to wav using pydub (optional if already converted)
    if file_path.lower().endswith('.m4a'):
        audio = AudioSegment.from_file(file_path, format='m4a')
        file_path = file_path.replace('.m4a', '.wav')
        audio.export(file_path, format='wav')

    try:
        with sr.AudioFile(file_path) as source:
            status_label.config(text="Listening to audio...")
            audio_data = recognizer.record(source)
            status_label.config(text="Transcribing...")
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.m4a")])
    if file_path:
        transcribed_text = transcribe_audio(file_path)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, transcribed_text)
        status_label.config(text="Done!")

# GUI setup
window = tk.Tk()
window.title("🎤 Speech-to-Text Transcriber")
window.geometry("600x400")
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="Speech-to-Text Tool", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

select_button = tk.Button(window, text="Select Audio File", command=select_file, bg="#4CAF50", fg="white", padx=10, pady=5)
select_button.pack(pady=10)

text_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
text_output.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

status_label = tk.Label(window, text="", font=("Arial", 10), fg="gray", bg="#f0f0f0")
status_label.pack(pady=5)

window.mainloop()