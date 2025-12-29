import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io

class U2NetMultiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Détourage multiple (U²-Net)")
        self.root.geometry("900x700")

        self.image = None
        self.tk_image = None
        self.result_image = None
        self.rectangles = []  # stocke tous les rectangles (coordonnées)
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        # Barre de commandes
        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        tk.Button(toolbar, text="Ouvrir une image", command=self.open_image).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Détourer tous les objets", command=self.run_u2net_all).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Enregistrer résultat", command=self.save_result).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Réinitialiser rectangles", command=self.clear_rectangles).pack(side=tk.LEFT)
        tk.Label(toolbar, text="Tracer plusieurs rectangles autour des objets à détourer, puis clique sur Détourer tous les objets").pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Événements souris
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
        self.image = Image.open(path).convert("RGBA")
        self.display_image(self.image)
        self.rectangles.clear()

    def display_image(self, image):
        image = image.copy()
        image.thumbnail((900, 600))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def on_press(self, event):
        if self.image is None:
            return
        self.start_x, self.start_y = event.x, event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.image is None:
            return
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        self.rectangles.append((x1, y1, x2, y2))
        print(f"Rectangle ajouté : {(x1, y1, x2, y2)}")

    def clear_rectangles(self):
        self.rectangles.clear()
        print("Tous les rectangles ont été supprimés.")
        if self.image is not None:
            self.display_image(self.image)

    def run_u2net_all(self):
        if self.image is None:
            print("Ouvre d'abord une image.")
            return
        if not self.rectangles:
            print("Trace au moins un rectangle avant de détourer.")
            return

        print("Détourage de plusieurs objets en cours...")
        scale_x = self.image.width / self.tk_image.width()
        scale_y = self.image.height / self.tk_image.height()

        full_result = Image.new("RGBA", self.image.size, (0, 0, 0, 0))

        for i, rect in enumerate(self.rectangles, start=1):
            x1 = int(min(rect[0], rect[2]) * scale_x)
            y1 = int(min(rect[1], rect[3]) * scale_y)
            x2 = int(max(rect[0], rect[2]) * scale_x)
            y2 = int(max(rect[1], rect[3]) * scale_y)

            cropped = self.image.crop((x1, y1, x2, y2))
            
            # Note: Background removal functionality has been removed
            # Simply paste the cropped region without background removal
            full_result.paste(cropped, (x1, y1))
            print(f"Objet {i} extracted.")

        self.result_image = full_result
        self.display_image(full_result)
        print("All objects have been extracted.")

    def save_result(self):
        if self.result_image is None:
            print("Aucun résultat à enregistrer.")
            return
        self.result_image.save("extraction_multi_u2net.png")
        print("Résultat sauvegardé : extraction_multi_u2net.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = U2NetMultiApp(root)
    root.mainloop()
