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



# LANCEMENT DE L'APPLICATION

app = customtkinter.CTk()
app.title("PYDL")
app.geometry("1500x500")


# SECTION CHARGEMENT DOSSIER

dossier_frame = customtkinter.CTkFrame(app)
dossier_frame.pack(fill=customtkinter.X, padx=10, pady=(20, 10))


welcome_label = customtkinter.CTkLabel(dossier_frame, text="Bonjour, avant de commencer à télécharger, sélectionnez le dossier où mettre les résultats")
welcome_label.pack(pady=(20,10))


dosTel_label = customtkinter.CTkLabel(dossier_frame, text="Dossier de téléchargement:")
dosTel_label.pack(pady=(20, 10))
dosTel_button = customtkinter.CTkButton(dossier_frame, text="Choisir Dossier", command=lambda: choose_directory())
dosTel_button.pack(pady=(20, 10))
dosTel_entry = tkinter.Entry(dossier_frame, width=50)
dosTel_entry.pack(pady=(20, 10))


main_frame = customtkinter.CTkFrame(app)
main_frame.pack(pady=20)


# SECTION YOUTUBE

formats = ["mp4", "mp3"]
qualites = ["1080p", "720p", "480p"]

format_var = customtkinter.StringVar(value="mp4")
qualite_var = customtkinter.StringVar(value="1080p")


youtube_frame = customtkinter.CTkFrame(main_frame)
youtube_frame.grid(row=0, column=0, padx=10, pady=10)

# Lien YouTube
youtube_label = customtkinter.CTkLabel(youtube_frame, text="Lien Youtube:")
youtube_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 10))

youtube_link_entry = tkinter.Entry(youtube_frame, width=50)
youtube_link_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 10))

# Format et Qualité
format_label = customtkinter.CTkLabel(youtube_frame, text="Format:")
format_label.grid(row=1, column=0, padx=(10, 5), pady=10)

format_combobox = customtkinter.CTkComboBox(master=youtube_frame, values=formats, variable=format_var)
format_combobox.grid(row=1, column=1, padx=(5, 10), pady=10)

quality_label = customtkinter.CTkLabel(youtube_frame, text="Qualité:")
quality_label.grid(row=2, column=0, padx=(10, 5), pady=10)

quality_combobox = customtkinter.CTkComboBox(youtube_frame, values=qualites, variable=qualite_var)
quality_combobox.grid(row=2, column=1, padx=(5, 10), pady=10)

# Bouton de téléchargement
download_button = customtkinter.CTkButton(youtube_frame, text="Télécharger", command=download_youtube)
download_button.grid(row=3, columnspan=2, pady=(30, 30))

# SECTION CONVERSION MP4 EN MP3


converter_frame = customtkinter.CTkFrame(main_frame)
converter_frame.grid(row=0, column=1, padx=10, pady=10)

mp4_label = customtkinter.CTkLabel(converter_frame, text="Convertisseur MP4 en MP3 :")
mp4_label.grid(row=0, column=1, padx=5, pady=(20, 10))

mp4_button = customtkinter.CTkButton(converter_frame, text="Choisir MP4", command=choose_mp4_file)
mp4_button.grid(row=1, column=1, padx=10, pady=(20, 10))

mp4_entry = tkinter.Entry(converter_frame, width=50)
mp4_entry.grid(row= 1, column=2, padx=10, pady=(20, 10))

convert_button = customtkinter.CTkButton(converter_frame, text="Convertir MP4 en MP3", command=mp4_to_mp3)
convert_button.grid(row=2, column=1, padx=10, pady=(20, 10))


# SECTION INSTAGRAM REEL

instagram_frame = customtkinter.CTkFrame(main_frame)
instagram_frame.grid(row=0, column=2, padx=10, pady=10)

insta_label = customtkinter.CTkLabel(instagram_frame, text="Lien Instagram Reel:")
insta_label.grid(row=0, column=0, padx=10, pady=(20, 10))

insta_link_entry = tkinter.Entry(instagram_frame, width=50)
insta_link_entry.grid(row=1, column=0, padx=10, pady=(20, 10))

insta_button = customtkinter.CTkButton(instagram_frame, text="Télécharger Reel Insta", command=lambda: downloadInsta(insta_link_entry.get()))
insta_button.grid(row=2, column=0, padx=10, pady=(20, 10))


app.mainloop()