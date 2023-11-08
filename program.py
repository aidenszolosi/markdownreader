import openai
import whisper
import tkinter as tk
from tkinter import simpledialog, filedialog

# Load your OpenAI API key from an environment variable or direct input
openai.api_key = 'your-api-key'

# Function to transcribe audio to text using Whisper-JAX and generate SRT
def transcribe_audio_to_srt(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path, verbose=False)
    segments = result['segments']
    
    srt_entries = []
    for i, segment in enumerate(segments):
        start = segment['start']
        end = segment['end']
        text = segment['text']
        srt_entries.append(f"{i+1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n")
    
    srt_content = "\n".join(srt_entries)
    return srt_content.split('\n\n'), srt_content  # Return as list of entries and full content

# Function to format timestamps for SRT
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')

# Function to identify and correct discrepancies using OpenAI
def correct_discrepancies(original_lyrics, transcribed_lyrics):
    corrected_lyrics = []
    for original, transcribed in zip(original_lyrics, transcribed_lyrics):
        if original.lower() != transcribed.lower():
            # Use OpenAI to suggest corrections
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Correct the transcribed lyrics to match the original lyrics:\nOriginal: {original}\nTranscribed: {transcribed}\nCorrected:",
                max_tokens=60
            )
            corrected = response.choices[0].text.strip()
            corrected_lyrics.append(corrected or original)
        else:
            corrected_lyrics.append(original)
    return corrected_lyrics

# Function to prompt user for original lyrics using a simple GUI
def get_original_lyrics_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    original_lyrics_text = simpledialog.askstring("Input", "Enter the original lyrics:", parent=root)
    return original_lyrics_text.split('\n') if original_lyrics_text else []

# Function to prompt user to select an audio file
def get_audio_file_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.ogg *.flac"), ("All Files", "*.*"))
    )
    return file_path

# Example usage
if __name__ == "__main__":
    # Get original lyrics from the user via GUI
    original_lyrics = get_original_lyrics_gui()

    # Get the audio file path from the user via GUI
    audio_file_path = get_audio_file_gui()

    # Transcribe the audio file and generate SRT content
    srt_entries, full_srt_content = transcribe_audio_to_srt(audio_file_path)

    # Save the SRT content to a file
    with open('transcription.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(full_srt_content)

    # Extract transcribed lyrics from SRT entries
    transcribed_lyrics = [entry.split('\n')[2] for entry in srt_entries]

    # Correct discrepancies
    corrected_lyrics = correct_discrepancies(original_lyrics, transcribed_lyrics)
    
    # Since we now have the SRT content, we can directly use it to create the LRC
    # Here we assume the SRT and original lyrics are line-aligned
    lrc_content = ""
    for srt_entry, corrected_lyric in zip(srt_entries, corrected_lyrics):
        start_time = srt_entry.split('\n')[1].split(' --> ')[0]
        lrc_timestamp = format_timestamp_for_lrc(start_time)
        lrc_content += f"{lrc_timestamp}{corrected_lyric}\n"

    # Save the LRC content to a file
    with open('song.lrc', 'w', encoding='utf-8') as lrc_file:
        lrc_file.write(lrc_content)

# Function to format timestamps for LRC
def format_timestamp_for_lrc(srt_timestamp):
    hours, minutes, seconds = srt_timestamp.split(':')
    seconds, milliseconds = seconds.split(',')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return f"[{total_seconds}.{int(milliseconds)//10}]"
