import os
import sys
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import subprocess
import datetime
from state_manager import save_state, load_state, clear_state

try:
    import whisper
except ImportError:
    messagebox.showerror(
        "Module manquant",
        "Le module 'openai-whisper' n'est pas installé.\nInstallez-le via 'pip install openai-whisper'."
    )
    raise

# === Dictionnaires ===
LANGUAGES_UI = {
    "fr": {
        "Automatique": None, "Anglais": "en", "Français": "fr", "Portugais": "pt", "Japonais": "ja",
        "Coréen": "ko", "Allemand": "de", "Espagnol": "es", "Hindi": "hi", "Arabe": "ar",
        "Mandarin (Chinois)": "zh", "Bengali": "bn", "Russe": "ru", "Punjabi (Lahnda occidental)": "pa",
        "Marathi": "mr", "Télougou": "te", "Turc": "tr", "Vietnamien": "vi", "Tamoul": "ta",
        "Urdu": "ur", "Javanais": "jv", "Bulgare": "bg", "Tchèque": "cs", "Danois": "da",
        "Néerlandais": "nl", "Estonien": "et", "Finnois": "fi", "Grec": "el", "Hongrois": "hu",
        "Irlandais": "ga", "Letton": "lv", "Lituanien": "lt", "Maltais": "mt", "Polonais": "pl",
        "Roumain": "ro", "Slovaque": "sk", "Slovène": "sl", "Suédois": "sv", "Croate": "hr"
    },
    "en": {
        "Automatic": None, "English": "en", "French": "fr", "Portuguese": "pt", "Japanese": "ja",
        "Korean": "ko", "German": "de", "Spanish": "es", "Hindi": "hi", "Arabic": "ar",
        "Mandarin (Chinese)": "zh", "Bengali": "bn", "Russian": "ru", "Punjabi (Western Lahnda)": "pa",
        "Marathi": "mr", "Telugu": "te", "Turkish": "tr", "Vietnamese": "vi", "Tamil": "ta",
        "Urdu": "ur", "Javanese": "jv", "Bulgarian": "bg", "Czech": "cs", "Danish": "da",
        "Dutch": "nl", "Estonian": "et", "Finnish": "fi", "Greek": "el", "Hungarian": "hu",
        "Irish": "ga", "Latvian": "lv", "Lithuanian": "lt", "Maltese": "mt", "Polish": "pl",
        "Romanian": "ro", "Slovak": "sk", "Slovenian": "sl", "Swedish": "sv", "Croatian": "hr"
    }
}

STRINGS = {
    "fr": {
        "title": "Transcription Audio → Texte",
        "choose": "Choisir fichier…",
        "transcribe": "Transcrire",
        "model_label": "Modèle de transcription :",
        "lang_label": "Langue de transcription :",
        "select_audio": "Sélectionnez un fichier audio",
        "finished": "Transcription terminée",
        "saved_in": "Transcription enregistrée dans :",
        "ffmpeg_missing": "Installez ffmpeg et ajoutez-le à votre PATH.",
        "error": "Erreur",
        "ffmpeg_error": "ffmpeg introuvable",
        "open_output": "Voir les transcriptions",
        "progress": "Transcription en cours",
        "ui_lang": "Langue de l’interface :"
    },
    "en": {
        "title": "Audio-to-Text Transcription",
        "choose": "Choose File…",
        "transcribe": "Transcribe",
        "model_label": "Whisper Model:",
        "lang_label": "Transcription Language:",
        "select_audio": "Select an audio file",
        "finished": "Finished",
        "saved_in": "Transcription saved in:",
        "ffmpeg_missing": "Please install ffmpeg and add it to your PATH.",
        "error": "Error",
        "ffmpeg_error": "ffmpeg not found",
        "open_output": "Open transcription folder",
        "progress": "Transcribing",
        "ui_lang": "Interface language:"
    }
}

# === Configuration ===

CONFIG_FILE = Path("config.json")

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_config(model, language):
    CONFIG_FILE.write_text(json.dumps({"model": model, "language": language}), encoding="utf-8")

config = load_config()
if "language" not in config:
    root_lang = tk.Tk()
    root_lang.title("Choix de langue")
    lang_choice = tk.StringVar(value="fr")
    tk.Radiobutton(root_lang, text="Français", variable=lang_choice, value="fr").pack()
    tk.Radiobutton(root_lang, text="English", variable=lang_choice, value="en").pack()

    def validate_lang():
        config["language"] = lang_choice.get()
        save_config(config.get("model", "small"), config["language"])
        root_lang.destroy()

    tk.Button(root_lang, text="OK", command=validate_lang).pack(pady=10)
    root_lang.mainloop()

config = load_config()
lang_key = config.get("language", "fr")
ui = STRINGS[lang_key]
lang_ui_list = LANGUAGES_UI[lang_key]

# === Fonctions ===

def select_file():
    file_paths = filedialog.askopenfilenames(
        title=ui["select_audio"],
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac"), ("All Files", "*.*")]
    )
    if file_paths:
        entry_path.set(" ".join(file_paths))

def transcribe_file(input_path, model_size="small", language=None, output_dir="output"):
    model = whisper.load_model(model_size)
    result = model.transcribe(input_path, language=language)
    text = result["text"].strip()
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = os.path.join(output_dir, f"{base}_{timestamp}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text, out_path

def animate_spinner():
    states = ["", ".", "..", "..."]
    idx = 0
    def update():
        nonlocal idx
        if not spinner_running:
            return
        lbl_spinner.config(text=ui["progress"] + states[idx % len(states)])
        idx += 1
        lbl_spinner.after(400, update)
    update()

def run_and_display(files):
    global spinner_running
    btn_transcribe.config(state=tk.DISABLED)
    txt_output.delete("1.0", tk.END)
    spinner_running = True
    animate_spinner()

    results = []
    for file in files.split():
        save_state(file, model_var.get(), lang_var.get())
        try:
            lang_code = lang_ui_list.get(lang_var.get())
            text, out_path = transcribe_file(file, model_var.get(), lang_code)
            results.append(out_path)
            if len(files.split()) == 1:
                txt_output.insert(tk.END, text + "\n")
        except FileNotFoundError:
            messagebox.showerror(ui["ffmpeg_error"], ui["ffmpeg_missing"])
        except Exception as e:
            messagebox.showerror(ui["error"], str(e))

    clear_state()
    spinner_running = False
    lbl_spinner.config(text=ui["finished"] + ".")
    btn_transcribe.config(state=tk.NORMAL)

    if results:
        message = "\n".join(results)
        messagebox.showinfo(ui["finished"], f"{ui['saved_in']}\n{message}")

    save_config(model_var.get(), lang_key)

def open_output_folder():
    output_dir = os.path.abspath("output")
    os.makedirs(output_dir, exist_ok=True)
    if sys.platform == "win32":
        os.startfile(output_dir)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", output_dir])
    else:
        subprocess.Popen(["xdg-open", output_dir])

def change_language(new_lang_key):
    save_config(model_var.get(), new_lang_key)
    subprocess.Popen([sys.executable] + sys.argv)  # redémarre l'app
    root.destroy()  # ferme proprement l’instance actuelle

# === Interface ===

root = tk.Tk()
root.title(ui["title"])
root.geometry("700x550")

# Changement langue UI
frame_lang = tk.Frame(root)
frame_lang.pack(anchor="nw", padx=10, pady=(5, 0))
tk.Label(frame_lang, text=ui["ui_lang"], font=("Helvetica", 9)).pack(side="left")
lang_ui = tk.StringVar(value=lang_key)
tk.OptionMenu(frame_lang, lang_ui, *STRINGS.keys(), command=change_language).pack(side="left")

entry_path = tk.StringVar()

tk.Button(root, text=ui["choose"], command=select_file).pack()
tk.Entry(root, textvariable=entry_path, width=60).pack(pady=10)

tk.Label(root, text=ui["model_label"]).pack()
model_var = tk.StringVar(value=config.get("model", "small"))
tk.OptionMenu(root, model_var, "tiny", "base", "small", "medium", "large").pack()

tk.Label(root, text=ui["lang_label"]).pack()
lang_var = tk.StringVar(value=list(lang_ui_list.keys())[0])
tk.OptionMenu(root, lang_var, *lang_ui_list.keys()).pack()

frame_transcribe = tk.Frame(root)
frame_transcribe.pack(pady=10)

btn_transcribe = tk.Button(
    frame_transcribe,
    text=ui["transcribe"],
    font=("Helvetica", 10, "bold"),
    command=lambda: threading.Thread(target=run_and_display, args=(entry_path.get(),)).start()
)
btn_transcribe.pack(side="left", padx=(0, 10))

lbl_spinner = tk.Label(
    frame_transcribe,
    text="",
    font=("Helvetica", 10, "italic"),
    width=25,
    anchor="w"
)
lbl_spinner.pack(side="left")

btn_open_folder = tk.Button(root, text=ui["open_output"], command=open_output_folder)
btn_open_folder.pack(anchor="e", padx=20, pady=(0, 5))

txt_output = tk.Text(root)
txt_output.pack(expand=True, fill="both")

spinner_running = False

root.mainloop()
