import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from pathlib import Path
from frame_extractor import FrameExtractor


class VideoFrameExtractorApp:
    """Application GUI pour extraire les frames d'une vidéo"""

    def __init__(self, root):
        self.root = root
        self.root.title("Extracteur de Frames Vidéo - 4K Enhancement")
        self.root.geometry("700x800")
        self.root.resizable(True, True)

        # Variables
        self.video_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.interval_var = tk.StringVar(value="1")
        self.resize_var = tk.BooleanVar(value=False)
        self.resize_width_var = tk.StringVar(value="")
        self.resize_height_var = tk.StringVar(value="")
        
        # Variables pour l'amélioration 4K
        self.upscale_4k_var = tk.BooleanVar(value=False)
        self.denoise_var = tk.BooleanVar(value=False)
        self.sharpen_var = tk.BooleanVar(value=False)
        self.contrast_var = tk.BooleanVar(value=False)
        self.saturation_var = tk.BooleanVar(value=False)

        self.extractor = None
        self.extraction_thread = None

        # Style
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.theme_use('clam')

        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets de l'interface"""

        # Créer un Canvas avec scrollbar
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Canvas principal
        self.canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame scrollable à l'intérieur du canvas
        main_frame = ttk.Frame(self.canvas, padding="15")
        self.canvas.create_window((0, 0), window=main_frame, anchor="nw", tags="main_frame")
        
        # Configuration du scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding pour la molette de souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Titre
        title_label = ttk.Label(main_frame, text="Extracteur de Frames Vidéo", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Sélection du fichier vidéo
        ttk.Label(main_frame, text="Vidéo source :").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.video_path, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Parcourir", command=self._select_video).grid(row=1, column=2, padx=5)

        # Sélection du dossier de sortie
        ttk.Label(main_frame, text="Dossier de sortie :").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=40).grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, text="Parcourir", command=self._select_output_dir).grid(row=2, column=2, padx=5)

        # Intervalle d'extraction
        ttk.Label(main_frame, text="Intervalle (secondes) :").grid(row=3, column=0, sticky=tk.W, pady=5)
        interval_spin = ttk.Spinbox(main_frame, from_=0.1, to=60, textvariable=self.interval_var, width=15)
        interval_spin.grid(row=3, column=1, sticky=tk.W, padx=5)

        # Redimensionnement
        ttk.Separator(main_frame, orient="horizontal").grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(main_frame, text="Redimensionnement (optionnel) :", font=("Arial", 10, "bold")).grid(
            row=5, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        ttk.Checkbutton(main_frame, text="Activer le redimensionnement", variable=self.resize_var,
                       command=self._toggle_resize).grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

        # Frame pour les options de redimensionnement
        resize_frame = ttk.Frame(main_frame)
        resize_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(resize_frame, text="Largeur (px) :").grid(row=0, column=0, sticky=tk.W)
        self.width_entry = ttk.Entry(resize_frame, textvariable=self.resize_width_var, width=15)
        self.width_entry.grid(row=0, column=1, padx=5)
        self.width_entry.config(state="disabled")

        ttk.Label(resize_frame, text="Hauteur (px) :").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.height_entry = ttk.Entry(resize_frame, textvariable=self.resize_height_var, width=15)
        self.height_entry.grid(row=0, column=3, padx=5)
        self.height_entry.config(state="disabled")

        # Améliorations 4K
        ttk.Separator(main_frame, orient="horizontal").grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(main_frame, text="Améliorations 4K :", font=("Arial", 10, "bold")).grid(
            row=9, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        # Frame pour les options d'amélioration
        enhancement_frame = ttk.Frame(main_frame)
        enhancement_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Checkbutton(enhancement_frame, text="Upscale 4K (3840x2160)", variable=self.upscale_4k_var).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(enhancement_frame, text="Débruitage", variable=self.denoise_var).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(enhancement_frame, text="Netteté avancée", variable=self.sharpen_var).grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(enhancement_frame, text="Améliorer contraste", variable=self.contrast_var).grid(row=3, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(enhancement_frame, text="Améliorer saturation", variable=self.saturation_var).grid(row=4, column=0, sticky=tk.W, pady=3)


        # Informations de la vidéo
        ttk.Separator(main_frame, orient="horizontal").grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(main_frame, text="Informations :", font=("Arial", 10, "bold")).grid(
            row=12, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        self.info_text = tk.Text(main_frame, height=4, width=65, wrap=tk.WORD, state="disabled", bg="white")
        self.info_text.grid(row=13, column=0, columnspan=3, padx=5, pady=5)

        # Barre de progression
        ttk.Separator(main_frame, orient="horizontal").grid(row=14, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(main_frame, text="Progression :").grid(row=15, column=0, columnspan=3, sticky=tk.W, pady=(5, 2))

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(main_frame, mode="determinate", variable=self.progress_var)
        self.progress_bar.grid(row=16, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.grid(row=16, column=2, sticky=tk.E, padx=(75, 5))

        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=17, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)

        self.start_button = ttk.Button(button_frame, text="Démarrer l'extraction", command=self._start_extraction)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Annuler", command=self._cancel_extraction, state="disabled")
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Ouvrir le dossier", command=self._open_output_folder).pack(side=tk.LEFT, padx=5)

        # Label de statut
        self.status_label = ttk.Label(main_frame, text="Prêt", relief="sunken")
        self.status_label.grid(row=18, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

        # Mettre à jour la région de scroll
        main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Gère le scroll avec la molette de souris"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(3, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-3, "units")

    def _toggle_resize(self):
        """Active/désactive les champs de redimensionnement"""
        state = "normal" if self.resize_var.get() else "disabled"
        self.width_entry.config(state=state)
        self.height_entry.config(state=state)

    def _select_video(self):
        """Ouvre un dialogue pour sélectionner la vidéo"""
        filetypes = (
            ("Tous les formats", "*.mp4 *.avi *.mov"),
            ("MP4", "*.mp4"),
            ("AVI", "*.avi"),
            ("MOV", "*.mov"),
            ("Tous les fichiers", "*.*")
        )

        filepath = filedialog.askopenfilename(
            title="Sélectionner une vidéo",
            filetypes=filetypes
        )

        if filepath:
            self.video_path.set(filepath)
            self._display_video_info(filepath)

    def _select_output_dir(self):
        """Ouvre un dialogue pour sélectionner le dossier de sortie"""
        dirpath = filedialog.askdirectory(title="Sélectionner le dossier de sortie")

        if dirpath:
            self.output_dir.set(dirpath)

    def _display_video_info(self, video_path):
        """Affiche les informations de la vidéo"""
        try:
            extractor = FrameExtractor(video_path, "")
            info = extractor.get_video_info()

            if info:
                duration = int(info['duration'])
                minutes = duration // 60
                seconds = duration % 60

                info_text = (
                    f"Résolution : {info['width']}x{info['height']}\n"
                    f"FPS : {info['fps']:.2f}\n"
                    f"Durée : {minutes}m {seconds}s\n"
                    f"Total frames : {info['total_frames']}"
                )
                self.info_text.config(state="normal")
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert("1.0", info_text)
                self.info_text.config(state="disabled")
            else:
                messagebox.showerror("Erreur", "Impossible de lire la vidéo")
                self.video_path.set("")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")
            self.video_path.set("")

    def _start_extraction(self):
        """Démarre l'extraction des frames"""
        # Validation
        if not self.video_path.get():
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une vidéo")
            return

        if not self.output_dir.get():
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un dossier de sortie")
            return

        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                messagebox.showwarning("Avertissement", "L'intervalle doit être positif")
                return
        except ValueError:
            messagebox.showwarning("Avertissement", "Intervalle invalide")
            return

        # Validation du redimensionnement
        resize_width = None
        resize_height = None

        if self.resize_var.get():
            if self.resize_width_var.get():
                try:
                    resize_width = int(self.resize_width_var.get())
                except ValueError:
                    messagebox.showwarning("Avertissement", "Largeur invalide")
                    return

            if self.resize_height_var.get():
                try:
                    resize_height = int(self.resize_height_var.get())
                except ValueError:
                    messagebox.showwarning("Avertissement", "Hauteur invalide")
                    return

            if not resize_width and not resize_height:
                messagebox.showwarning("Avertissement", "Entrez au moins une dimension")
                return

        # Désactiver les boutons
        self.start_button.config(state="disabled")
        self.cancel_button.config(state="normal")

        # Créer l'extracteur
        self.extractor = FrameExtractor(
            self.video_path.get(),
            self.output_dir.get(),
            interval,
            resize_width,
            resize_height,
            upscale_4k=self.upscale_4k_var.get(),
            denoise=self.denoise_var.get(),
            sharpen=self.sharpen_var.get(),
            enhance_contrast=self.contrast_var.get(),
            enhance_saturation=self.saturation_var.get()
        )

        # Démarrer l'extraction dans un thread
        self.extraction_thread = threading.Thread(target=self._run_extraction)
        self.extraction_thread.daemon = True
        self.extraction_thread.start()

    def _run_extraction(self):
        """Lance l'extraction dans un thread"""
        try:
            self.status_label.config(text="Extraction en cours...")
            self.root.update()

            extracted_count = self.extractor.extract_frames(self._update_progress)

            if not self.extractor.is_cancelled:
                self.progress_var.set(100)
                self.progress_label.config(text="100%")
                self.status_label.config(text=f"Extraction terminée : {extracted_count} frames extraites")
                messagebox.showinfo("Succès", f"{extracted_count} frames ont été extraites avec succès!")
            else:
                self.status_label.config(text="Extraction annulée")
                messagebox.showinfo("Annulation", "L'extraction a été annulée")

        except Exception as e:
            self.status_label.config(text="Erreur")
            messagebox.showerror("Erreur", f"Erreur lors de l'extraction : {str(e)}")

        finally:
            # Réactiver les boutons
            self.start_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.progress_var.set(0)
            self.progress_label.config(text="0%")

    def _update_progress(self, current_frame, total_frames, frame_path):
        """Met à jour la barre de progression"""
        if total_frames > 0:
            progress = int((current_frame / total_frames) * 100)
            self.progress_var.set(progress)
            self.progress_label.config(text=f"{progress}%")
            self.root.update_idletasks()

    def _cancel_extraction(self):
        """Annule l'extraction"""
        if self.extractor:
            self.extractor.cancel()
            self.cancel_button.config(state="disabled")

    def _open_output_folder(self):
        """Ouvre le dossier de sortie"""
        output_dir = self.output_dir.get()

        if not output_dir:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un dossier de sortie")
            return

        if not os.path.exists(output_dir):
            messagebox.showwarning("Avertissement", "Le dossier n'existe pas")
            return

        # Ouvrir le dossier
        import subprocess
        import sys

        if sys.platform == "win32":
            os.startfile(output_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", output_dir])
        else:
            subprocess.Popen(["xdg-open", output_dir])


def main():
    root = tk.Tk()
    app = VideoFrameExtractorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
