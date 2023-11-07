# AI Lyrics Transcription and Correction Program Guide

Welcome to the guide for creating a program that leverages AI to transcribe audio to text, compares the transcription to original lyrics, corrects any discrepancies, and converts the corrected lyrics into the LRC format. This guide is designed for users of all levels, including beginners.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Prepare Your Development Environment](#prepare-your-development-environment)
- [Transcription Process](#transcription-process)
- [SRT File Handling](#srt-file-handling)
- [Lyrics Comparison and Correction](#lyrics-comparison-and-correction)
- [LRC Format Conversion](#lrc-format-conversion)
- [Testing](#testing)
- [Deployment](#deployment)
- [Support and Troubleshooting](#support-and-troubleshooting)

## Introduction

This program is your assistant in creating synchronized lyrics files for music tracks. It will help you transcribe lyrics from audio, align them with the music's timing, and ensure they are accurate when compared to the original lyrics.

## Prerequisites

Before we start, you'll need:

- **Python**: Make sure Python 3.x is installed on your computer. If not, download it from the [Python official website](https://www.python.org/downloads/).
- **Text Editor**: Any basic text editor will do, but if you want suggestions, [Visual Studio Code](https://code.visualstudio.com/) is a great option.
- **Command Line Basics**: Familiarity with basic command line operations will be helpful.

## Installation

First, we need to set up our tools:

1. **Install Whisper-JAX**:

    Open your command line interface (CLI) and run:

    ```shell
    pip install whisper-jax
    ```

    This command installs the Whisper-JAX library, which we'll use for audio transcription.

## Prepare Your Development Environment

Before diving into the coding part, it's essential to set up a proper development environment. This will be your workspace where you'll write code, test your program, and debug any issues that arise.

1. **Choose a Text Editor or IDE**:
   
   A text editor is where you'll write your code. Choose one that you're comfortable with. If you're not sure where to start, here are a few options:
   
   - [Visual Studio Code](https://code.visualstudio.com/): A powerful, free editor that supports Python and many other languages.
   - [Sublime Text](https://www.sublimetext.com/): A fast and lightweight text editor with a lot of features.
   - [Atom](https://atom.io/): An open-source text editor that's modern, approachable, and hackable to the core.
   
   Download and install the text editor of your choice.

2. **Install Python**:
   
   If you haven't already, make sure Python is installed on your system. Python 3.x is recommended. You can download it from the [official Python website](https://www.python.org/downloads/). Follow the installation instructions for your operating system.

3. **Set Up a Project Folder**:
   
   Create a folder on your computer where you'll store all the files related to this project. You can name it something like `lyrics_transcription_project`. Here's how you can do it on different operating systems:

   - **Windows**:
     Right-click in your desired directory, select "New", then "Folder", and name it.
   
   - **macOS/Linux**:
     Use the `mkdir` command in the terminal, like so:
     ```shell
     mkdir lyrics_transcription_project
     ```

4. **Create a Virtual Environment** (Optional but Recommended):
   
   A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. This allows you to manage dependencies for your project and ensure that it's isolated from other Python projects. Here's how to create one:

   - Open your command line interface (CLI).
   - Navigate to your project folder:
     ```shell
     cd path_to_your_project_folder
     ```
   - Run the following command to create a virtual environment:
     ```shell
     python -m venv venv
     ```
   - To activate the virtual environment:
     - **Windows**:
       ```shell
       venv\Scripts\activate
       ```
     - **macOS/Linux**:
       ```shell
       source venv/bin/activate
       ```
   
   When the virtual environment is activated, you'll see its name in the command prompt. Now, any Python packages you install while the virtual environment is active will only affect this project.

5. **Install Required Packages**:

   With your virtual environment activated, install the necessary Python packages. For now, we'll start with Whisper-JAX:

   ```shell
   pip install whisper-jax
   
  ## Transcription Process

We'll start by transcribing audio files to text. Create a new Python file named `transcribe.py` and use the following script:

```python
import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    print(result["text"])

transcribe_audio('path_to_your_audio_file.mp3')
```
Replace 'path_to_your_audio_file.mp3' with the actual path to your audio file.

## Lyrics Comparison and Correction
After transcribing, compare the AI-generated transcription with the original lyrics to correct any discrepancies.

Comparison Logic
Develop logic that compares each line of the AI-generated transcription with the corresponding line of the original lyrics.

Implementing Comparison Logic
Add a new function to your transcribe.py script to perform the comparison:


```python
def compare_lyrics(original_lyrics, transcribed_lyrics):
    for line_number, (original, transcribed) in enumerate(zip(original_lyrics, transcribed_lyrics), start=1):
        if original.strip() != transcribed.strip():
            print(f"Discrepancy found on line {line_number}:")
            print(f"Original: {original}")
            print(f"Transcribed: {transcribed}")
            print("\n")

# Example usage:
original_lyrics = ["Hello darkness, my old friend", "I've come to talk with you again"]
transcribed_lyrics = ["Hello darkness, my old friend", "I've come to walk with you again"]  # Notice the mistake in the second line

compare_lyrics(original_lyrics, transcribed_lyrics)
```
## LRC Format Conversion
Convert the corrected lyrics into the LRC format. Create a function named convert_to_lrc that formats each line according to the LRC standard.

```python
def convert_to_lrc(corrected_lyrics_with_timestamps, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for timestamp, lyric in corrected_lyrics_with_timestamps:
            # Convert SRT timestamp to LRC timestamp
            hours, minutes, seconds = timestamp.split(':')
            seconds, milliseconds = seconds.split(',')
            lrc_timestamp = f"[{int(hours) * 60 + int(minutes)}:{seconds}.{int(milliseconds)//10}]"
            
            # Write the LRC-formatted line to the file
            file.write(f"{lrc_timestamp} {lyric}\n")

# Example usage:
corrected_lyrics_with_timestamps = [
    ("00:00:01,000", "Hello darkness, my old friend"),
    ("00:00:04,000", "I've come to talk with you again")
]

convert_to_lrc(corrected_lyrics_with_timestamps, 'song.lrc')
```

### Testing
- Test your program thoroughly to ensure accuracy and reliability.

### Run Tests
- Transcription Accuracy: Test with various audio files to ensure the transcription is accurate.
Synchronization: Check that the timestamps match the audio segments correctly.
Correction Efficiency: Assess how well your program corrects discrepancies between the AI-generated transcription and the original lyrics.
- LRC Format Compatibility: Validate that the LRC files are compatible with media players.
- Automated Testing
Implement automated tests to streamline the testing process and ensure that your program remains reliable as you make changes.

## Deployment
- Choose the best deployment option for your program, whether it's a web-based application or a standalone program. Consider the ease of use for the end-user and the resources required to maintain the application.

## Support and Troubleshooting
- Provide comprehensive support and troubleshooting resources to help users resolve any issues they encounter.

## Documentation
- Create a user manual, FAQs, and a troubleshooting guide to assist users in navigating the program and resolving common issues.

## Feedback Loop
- Establish a feedback loop for users to report bugs and request new features. This will help you improve the program over time.

## Updates and Maintenance
- Plan for regular updates to the program and keep users informed about new versions and features.
