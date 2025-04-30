# 🎙️ Audio-to-Text Transcription with Whisper and Tkinter

This user-friendly Python application converts audio files (MP3, WAV, M4A, FLAC, etc.) into text using OpenAI’s Whisper model via a simple, multilingual Tkinter GUI.

---

## 🚀 Key Features

- 🌐 **Multilingual interface**:
  - Full support for **English** and **French** UI.
  - Over 30 transcription languages available.
  - 🔄 **Dynamic language switching**: Change interface language live from the dropdown (top left), or during first startup via popup.
- 📁 **Multi-file support**: Select and transcribe multiple audio files at once.
- 🧠 **Smart model selection**: Choose from Whisper models: `tiny`, `base`, `small`, `medium`, `large`.
- 📦 **Auto-saving**:
  - Files are saved with **timestamped filenames**.
  - Results are stored in the `output/` folder.
- 🌀 **Progress feedback**:
  - A spinner animates while transcribing.
  - Status label changes from `"Transcribing..."` to `"Finished."`.
- 📂 **Output access**:
  - Click **View transcriptions** to open the output folder.
  - Transcriptions are also shown live in the interface.
- 🔧 **Persistent preferences**:
  - Last selected model and language are saved in a local `config.json` file.
- ⚙️ **Lightweight and easy to install**.

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
.venv\Scripts\activate         # Windows
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

1. **Choose file(s)**: Click the **Choose File…** button. Multiple file selection is supported.
2. **Model**: Pick a Whisper model (`tiny`, `base`, `small`, etc.).
3. **Transcription language**:
   - Choose **Automatic** or select a specific language.
4. **Click Transcribe**: Wait while processing.
5. **View results**:
   - Transcription text appears in the interface.
   - Output is saved in the `output/` folder.
6. **Change UI language**:
   - Use the **interface language selector** (top-left) to switch between French/English.

---

## Roadmap
✅ Phase 1 — Core Features (Completed)

    Error recovery
    → Resumes an interrupted transcription session using saved state.
    Status: ✅ Implemented

    Batch transcription
    → Allows selection of multiple audio files and processes them sequentially.
    Status: ✅ Implemented

    Persistent configuration
    → Stores user preferences (Whisper model, transcription language) in config.json.
    Status: ✅ Implemented

✅ Phase 2 — Technical and Maintenance (Completed)

    Memory release (GPU/CPU)
    → Releases resources after transcription to avoid overload.
    Status: ✅ Implemented

    Model update check
    → Checks for Whisper model updates and notifies the user.
    Status: ❌ Dropped (feature removed at your request)

    Offline mode with preloaded models
    → Allows Whisper to run without internet using locally available models.
    Status: ✅ Implemented (via whisper default behavior if models are cached)

    Automatic ffmpeg verification
    → Checks if ffmpeg is available at launch, displays error otherwise.
    Status: ✅ Implemented

🟡 Phase 3 — Developer Experience (In Progress)

    Docstrings for all functions
    → Improves readability and maintainability.
    Status: 🔄 Planned

    Type annotations (type hints)
    → Clarifies expected argument and return types.
    Status: 🔄 Planned

    Modular code structure
    → Separates logic into distinct files: UI, transcription engine, configuration.
    Status: 🔄 Planned

---

## 📖 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

