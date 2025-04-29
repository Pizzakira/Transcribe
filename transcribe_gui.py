import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys

try:
    import whisper
except ImportError:
    messagebox.showerror(
        "Module manquant",
        "Le module 'openai-whisper' n'est pas installé.\nInstallez-le via 'pip install openai-whisper'."
    )
    raise

LANGUAGES_UI = {
    "fr": {"Automatique": None, "Anglais": "en", "Français": "fr", "Portugais": "pt", "Japonais": "ja", "Coréen": "ko", "Allemand": "de", "Espagnol": "es", "Hindi": "hi", "Arabe": "ar", "Mandarin (Chinois)": "zh", "Bengali": "bn", "Russe": "ru", "Punjabi (Lahnda occidental)": "pa", "Marathi": "mr", "Télougou": "te", "Turc": "tr", "Vietnamien": "vi", "Tamoul": "ta", "Urdu": "ur", "Javanais": "jv", "Bulgare": "bg", "Tchèque": "cs", "Danois": "da", "Néerlandais": "nl", "Estonien": "et", "Finnois": "fi", "Grec": "el", "Hongrois": "hu", "Irlandais": "ga", "Letton": "lv", "Lituanien": "lt", "Maltais": "mt", "Polonais": "pl", "Roumain": "ro", "Slovaque": "sk", "Slovène": "sl", "Suédois": "sv", "Croate": "hr"},
    "en": {"Automatic": None, "English": "en", "French": "fr", "Portuguese": "pt", "Japanese": "ja", "Korean": "ko", "German": "de", "Spanish": "es", "Hindi": "hi", "Arabic": "ar", "Mandarin (Chinese)": "zh", "Bengali": "bn", "Russian": "ru", "Punjabi (Western Lahnda)": "pa", "Marathi": "mr", "Telugu": "te", "Turkish": "tr", "Vietnamese": "vi", "Tamil": "ta", "Urdu": "ur", "Javanese": "jv", "Bulgarian": "bg", "Czech": "cs", "Danish": "da", "Dutch": "nl", "Estonian": "et", "Finnish": "fi", "Greek": "el", "Hungarian": "hu", "Irish": "ga", "Latvian": "lv", "Lithuanian": "lt", "Maltese": "mt", "Polish": "pl", "Romanian": "ro", "Slovak": "sk", "Slovenian": "sl", "Swedish": "sv", "Croatian": "hr"}
}

STRINGS = {
    "fr": {
        "title": "Transcription Audio → Texte",
        "choose": "Choisir fichier…",
        "transcribe": "Transcrire",
        "model_label": "Modèle de transcription:",
        "lang_label": "Langue de transcription:",
        "select_audio": "Sélectionnez un fichier audio",
        "finished": "Transcription terminée",
        "saved_in": "Transcription enregistrée dans:",
        "ffmpeg_missing": "Installez ffmpeg et ajoutez-le à votre PATH.",
        "error": "Erreur",
        "ffmpeg_error": "ffmpeg introuvable",
        "open_output": "Voir les transcriptions",
        "progress": "Transcription en cours"
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
        "progress": "Transcribing"
    }
}

root_lang = tk.Tk()
root_lang.title("Choose Language / Choisir la langue")
lang_choice = tk.StringVar(value="fr")
tk.Radiobutton(root_lang, text="Français", variable=lang_choice, value="fr").pack()
tk.Radiobutton(root_lang, text="English", variable=lang_choice, value="en").pack()
tk.Button(root_lang, text="OK", command=root_lang.destroy).pack(pady=10)
root_lang.mainloop()

ui = STRINGS[lang_choice.get()]
lang_ui_list = LANGUAGES_UI[lang_choice.get()]

def select_file():
    file_path = filedialog.askopenfilename(
        title=ui["select_audio"],
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac"), ("All Files", "*.*")]
    )
    if file_path:
        entry_path.set(file_path)

def transcribe_file(input_path, model_size="small", language=None, output_dir="output"):
    model = whisper.load_model(model_size)
    result = model.transcribe(input_path, language=language)
    text = result["text"].strip()
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_path))[0]
    i = 0
    while os.path.exists(out_path := os.path.join(output_dir, f"{base}_{i}.txt")):
        i += 1
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

def run_and_display(file):
    global spinner_running
    btn_transcribe.config(state=tk.DISABLED)
    txt_output.delete("1.0", tk.END)
    spinner_running = True
    animate_spinner()
    try:
        lang_code = lang_ui_list.get(lang_var.get())
        text, out_path = transcribe_file(file, model_var.get(), lang_code)
        txt_output.insert(tk.END, text)
        messagebox.showinfo(ui["finished"], f"{ui['saved_in']}\n{out_path}")
    except FileNotFoundError:
        messagebox.showerror(ui["ffmpeg_error"], ui["ffmpeg_missing"])
    except Exception as e:
        messagebox.showerror(ui["error"], str(e))
    finally:
        spinner_running = False
        lbl_spinner.config(text=ui["finished"] + ".")
        btn_transcribe.config(state=tk.NORMAL)

def open_output_folder():
    output_dir = os.path.abspath("output")
    os.makedirs(output_dir, exist_ok=True)
    if sys.platform == "win32":
        os.startfile(output_dir)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", output_dir])
    else:
        subprocess.Popen(["xdg-open", output_dir])

root = tk.Tk()
root.title(ui["title"])
root.geometry("700x550")

entry_path = tk.StringVar()

tk.Button(root, text=ui["choose"], command=select_file).pack()
tk.Entry(root, textvariable=entry_path, width=60).pack(pady=10)

tk.Label(root, text=ui["model_label"]).pack()
model_var = tk.StringVar(value="small")
tk.OptionMenu(root, model_var, "tiny", "base", "small", "medium", "large").pack()

tk.Label(root, text=ui["lang_label"]).pack()
lang_var = tk.StringVar(value=list(lang_ui_list.keys())[0])
tk.OptionMenu(root, lang_var, *lang_ui_list.keys()).pack()

frame_transcribe = tk.Frame(root)
frame_transcribe.pack(pady=10)

btn_transcribe = tk.Button(
    frame_transcribe,
    text=ui["transcribe"],
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
