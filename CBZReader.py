import tkinter as tk
import zipfile
from tkinter import filedialog
from PIL import Image, ImageTk


class MyReader:
    def __init__(self, master):
        # Demande à l'user de choisir son fichier .cbz
        archive = filedialog.askopenfilename(filetypes=[("Comic Book Archive", "*.cbz")])

        # Extraire l'archive cbz
        with zipfile.ZipFile(archive, 'r') as cbz:
            images = [Image.open(cbz.open(name)) for name in cbz.namelist() if name.endswith(('jpg', 'jpeg', 'png', 'gif'))]

        # Initialiser la fenêtre principale
        self.master = master
        self.master.title("P4radox CBZ Reader")
        self.master.resizable(True, True)

        # Canvas pour l'affichage des images
        self.canvas = tk.Canvas(self.master, width=600, height=800)
        self.canvas.pack()

        # Vars
        self.images = images
        self.current_image_index = 0
        self.zoom_factor = 1.0

        # Affiche les images
        self.show_image()

        # Navigation
        prev_button = tk.Button(self.master, text="Précédent", command=self.prev_image)
        prev_button.pack(side=tk.LEFT, padx=10)
        next_button = tk.Button(self.master, text="Suivant", command=self.next_image)
        next_button.pack(side=tk.RIGHT, padx=10)

        # Add a zoom slider
        zoom_scale = tk.Scale(self.master, from_=10, to=200, orient=tk.HORIZONTAL, label="Zoom (%)",
                              command=self.zoom_image)
        zoom_scale.pack(side=tk.BOTTOM, fill=tk.X)

        # Set default zoom to 100%
        zoom_scale.set(100)

    def show_image(self):
        # Bye canvas
        self.canvas.delete("all")

        # Affiche l'image en cours
        image = self.images[self.current_image_index]
        image = image.resize((int(image.width * self.zoom_factor), int(image.height * self.zoom_factor)), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def prev_image(self):
        # Image précedente
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def next_image(self):
        # Image suivante
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()

    def zoom_image(self, zoom):
        # Get current image and scale factor
        image = self.images[self.current_image_index]
        self.zoom_factor = float(zoom) / 100

        # Resize image with new scale factor
        width = int(image.width * self.zoom_factor)
        height = int(image.height * self.zoom_factor)
        image = image.resize((width, height), Image.ANTIALIAS)

        # Update canvas with new image
        photo = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo


# Main window
mainWin = tk.Tk()

# Lance l'app
app = MyReader(mainWin)

# Loop l'app jusqu'a fermeture
mainWin.mainloop()