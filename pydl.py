import time
import tkinter
from tkinter import filedialog, messagebox

import customtkinter
from instascrape import Reel
from moviepy.editor import *
from pytube import YouTube


def extraction_nom_fichier(path):
    """Extracts the name of the file from the path."""
    return os.path.splitext(os.path.basename(path))[0]

def mp4_to_mp3():
    """Converts an mp4 file to an mp3 file."""

    # Récupère le chemin du fichier mp4 depuis le label
    file_path = mp4_entry.get()

    # Récupère le chemin du dossier de téléchargement
    output_directory = dosTel_entry.get()

    # Créer le chemin complet pour le fichier de sortie mp3
    nom = extraction_nom_fichier(file_path) + ".mp3"  # Nom du fichier MP3
    audio_path = os.path.join(output_directory, nom)

    # Charger le clip vidéo
    video = VideoFileClip(file_path)

    # Écrire l'audio dans un fichier MP3
    video.audio.write_audiofile(audio_path)

    messagebox.showinfo("Status", "Conversion completed successfully.")



def create_header():
    """Create and return the header dictionary."""
    SESSIONID = "1519068478%3AIKoa5CtY6SPUEO%3A16%3AAYcVvb-G-en49kcs-IS2oLaJcWaK6kNxEb6Z2UkXPg"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        "cookie": f'sessionid={SESSIONID};'
    }

    print(headers)

    return headers


def downloadInsta(link):
    try:
        if link:
            headers = create_header()
            print("test headers")

            reel = Reel(link)
            print("test reels")
            reel.scrape(headers=headers)
            print("test scrape")
            reel.download(fp=f".\\reel{int(time.time())}.mp4")
            print("test dl")
            messagebox.showinfo("Status", "Reel downloaded successfully")
        else:
            messagebox.showwarning("Empty field", "Please fill out the field")
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong. Please try again later.")


def choose_mp4_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        mp4_entry.delete(0, tkinter.END)  # Clear the current content
        mp4_entry.insert(0, file_path)  # Insert the new file path in the Entry


def choose_directory():
    """Choose the directory where the video will be downloaded."""
    directory_path = filedialog.askdirectory()
    if directory_path:
        dosTel_entry.delete(0, tkinter.END)  # Supprime le contenu actuel
        dosTel_entry.insert(0, directory_path)  # Insère le nouveau chemin dans le Entry


def download_youtube():
    """Download YouTube video based on user inputs."""
    url = youtube_link_entry.get()
    directory_path = dosTel_entry.get()  # Récupère le chemin du dossier depuis le label

    # Récupère les valeurs sélectionnées dans les combobox
    format_var = format_combobox.get()
    qualite_var = quality_combobox.get()

    if not url or not directory_path or not format_var or not qualite_var:
        messagebox.showwarning("Incomplete Information", "Please provide all required information.")
        return

    yt = YouTube(url)


    if format_var == "mp4":
        video_stream = yt.streams.filter(resolution=qualite_var).first()
        if video_stream:
            video_stream.download(directory_path)
        else:
            messagebox.showerror("Error", "No MP4 stream available for the selected quality.")
            return
    elif format_var == "mp3":
        video = yt.streams.filter(only_audio=True).first()
        destination = directory_path
        out_file = video.download(output_path=destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    messagebox.showinfo("Status", "Download completed successfully.")



app = customtkinter.CTk()
app.title("PYDL")
app.geometry("1000x500")


# Download Directory Section
dosTel_label = customtkinter.CTkLabel(app, text="Dossier de téléchargement:")
dosTel_label.grid(row=0, column=0, padx=10, pady=(20, 10))
dosTel_button = customtkinter.CTkButton(app, text="Choisir Dossier", command=lambda: choose_directory())
dosTel_button.grid(row=0, column=1, padx=10, pady=(20, 10))
dosTel_entry = tkinter.Entry(app, width=50)
dosTel_entry.grid(row=0, column=2, padx=10, pady=(20, 10))



# --- YouTube Section ---
youtube_label = customtkinter.CTkLabel(app, text="Lien Youtube:")
youtube_label.grid(row=1, column=0, padx=10, pady=(10, 10))

# Download Button
download_button = customtkinter.CTkButton(app, text="Télécharger", command=download_youtube)
download_button.grid(row=1, column=2, padx=10, pady=(30, 30))

youtube_link_entry = tkinter.Entry(app, width=50)
youtube_link_entry.grid(row=1, column=1, padx=10, pady=(10, 10))

# Options pour le format et la qualité

formats = ["mp4", "mp3"]
qualites = ["1080p", "720p", "480p"]

# Variables pour stocker les choix

format_var = customtkinter.StringVar(value="mp4")  # set initial value
qualite_var = customtkinter.StringVar(value="1080p")

format_label = customtkinter.CTkLabel(app, text="Format:")
format_label.grid(row=2, column=0, padx=10, pady=(10, 10))

quality_label = customtkinter.CTkLabel(app, text="Qualité:")
quality_label.grid(row=3, column=0, padx=10, pady=(10, 10))

# Combobox pour le format
format_combobox = customtkinter.CTkComboBox(master=app, values=formats, variable=format_var)
format_combobox.grid(row=2, column=1)

# Combobox pour la qualité
quality_combobox = customtkinter.CTkComboBox(app, values=qualites, variable=qualite_var)
quality_combobox.grid(row=3, column=1)



# --- MP4 to MP3 Section ---
# Choose MP3 File Section
mp4_label = customtkinter.CTkLabel(app, text="Fichier MP4 :")
mp4_label.grid(row=4, column=0, padx=10, pady=(20, 10))

mp4_button = customtkinter.CTkButton(app, text="Choisir MP4", command=choose_mp4_file)
mp4_button.grid(row=4, column=1, padx=10, pady=(20, 10))

mp4_entry = tkinter.Entry(app, width=50)
mp4_entry.grid(row=4, column=2, padx=10, pady=(20, 10))

convert_button = customtkinter.CTkButton(app, text="Convertir MP4 en MP3", command=mp4_to_mp3)
convert_button.grid(row=4, column=3, padx=10, pady=(20, 10))



# --- Instagram Reel Section ---
insta_label = customtkinter.CTkLabel(app, text="Lien Instagram Reel:")
insta_label.grid(row=5, column=0, padx=10, pady=(20, 10))

insta_link_entry = tkinter.Entry(app, width=50)
insta_link_entry.grid(row=5, column=1, padx=10, pady=(20, 10))

insta_button = customtkinter.CTkButton(app, text="Télécharger Reel Insta", command=lambda: downloadInsta(insta_link_entry.get()))
insta_button.grid(row=5, column=2, padx=10, pady=(20, 10))


app.mainloop()