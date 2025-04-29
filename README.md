# 🎙️ Audio-to-Text Transcription with Whisper and Tkinter

This user-friendly Python application converts audio files (MP3, WAV, M4A, FLAC, etc.) into text using OpenAI’s Whisper model via a simple, multilingual Tkinter GUI.

---

## 🚀 Key Features

- 🌐 **Multilingual interface**: English and French support, with over 30 transcription languages available.
- 🎛️ **Model selection**: Easily choose from Whisper models (`tiny`, `base`, `small`, `medium`, `large`).
- 📁 **Smart output handling**: Transcriptions are automatically saved in an `output/` folder with unique filenames.
- ⏳ **Progress feedback**: A spinner next to the **Transcribe** button displays `"Transcribing..."` during processing, then switches to `"Finished."` when done.
- 🗂️ **Direct access to results**: A **View transcriptions** button opens the output folder in your file explorer.
- 🔄 **Auto language detection** or manual selection.
- ⚙️ **Lightweight and easy to set up**.

---

## 📋 Prerequisites

- **Python ≥ 3.8**
- **Whisper** speech-to-text engine:

```bash
pip install openai-whisper
```

- **FFmpeg** (required for audio decoding):

### Windows

```bash
winget install ffmpeg
```
Or download manually from [ffmpeg.org](https://ffmpeg.org/) and add the `bin` folder to your system `PATH`.

### Linux/macOS

```bash
sudo apt install ffmpeg  # Debian/Ubuntu
brew install ffmpeg      # macOS (with Homebrew)
```

---

## 🛠️ Installation

1. Clone this repository:

```bash
git clone https://github.com/Pizzakira/Transcribe
cd transcribe
```

2. (Optional) Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate       # Windows
```

3. Install dependencies:

```bash
pip install openai-whisper
```

4. Verify FFmpeg is installed:

```bash
ffmpeg -version
```

---

## ▶️ How to Use

### Launch the app

- **Windows**: Double-click `transcribe_gui.py` or create a `.bat` file.
- **macOS/Linux**:

```bash
python transcribe_gui.py
```

### Step-by-step guide

1. **Choose an audio file**: Click the **Choose File…** button.
2. **Select a Whisper model**: Choose from the dropdown (`small` is default).
3. **Select transcription language**: Choose **Automatic** or manually select a language.
4. **Click Transcribe**: Processing may take some time depending on audio length and model.
5. **Follow progress**:
   - A spinner appears next to the button showing `"Transcribing..."`.
   - It switches to `"Finished."` when done.
6. **View results**:
   - Transcribed text is displayed in the text box.
   - A `.txt` file is saved in the `output/` folder.
   - Click **View transcriptions** to open the folder directly.

---

## 📖 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📝 License

Open-source project under the MIT License.
