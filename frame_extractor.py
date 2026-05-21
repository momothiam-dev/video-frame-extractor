import cv2
import os
import threading
import numpy as np
from pathlib import Path
from datetime import timedelta


class ImageEnhancer:
    """Classe pour améliorer les images en haute résolution (4K)"""

    @staticmethod
    def upscale_to_4k(image, target_width=3840, target_height=2160):
        """
        Upscale une image vers 4K (3840x2160)
        
        Args:
            image: Image source
            target_width: Largeur cible (défaut 3840 - 4K)
            target_height: Hauteur cible (défaut 2160 - 4K)
            
        Returns:
            Image upscalée
        """
        height, width = image.shape[:2]
        
        # Calculer le ratio d'aspect
        aspect_ratio = width / height
        target_aspect = target_width / target_height
        
        if aspect_ratio > target_aspect:
            # Adapter la hauteur
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Adapter la largeur
            new_height = target_height
            new_width = int(target_height * aspect_ratio)
        
        # Upscaler avec interpolation LANCZOS4 (meilleure qualité)
        upscaled = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        return upscaled

    @staticmethod
    def denoise(image, strength=10):
        """
        Réduit le bruit de l'image
        
        Args:
            image: Image source
            strength: Force du débruitage (1-30)
            
        Returns:
            Image débruitée
        """
        return cv2.fastNlMeansDenoisingColored(image, None, h=strength, templateWindowSize=7, searchWindowSize=21)

    @staticmethod
    def enhance_sharpness(image, strength=1.5):
        """
        Améliore la netteté de l'image
        
        Args:
            image: Image source
            strength: Force de la netteté (1.0-3.0)
            
        Returns:
            Image affinée
        """
        # Créer un noyau de netteté
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]) / 1.0
        
        # Appliquer le filtre de netteté
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Blender l'image originale et l'image affinée
        result = cv2.addWeighted(image, 1.0, sharpened - image, strength - 1.0, 0)
        
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def enhance_contrast(image, strength=1.2):
        """
        Améliore le contraste de l'image
        
        Args:
            image: Image source
            strength: Force du contraste (1.0-2.0)
            
        Returns:
            Image avec contraste amélioré
        """
        # Convertir en LAB pour mieux contrôler le contraste
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Appliquer CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=strength * 2.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        
        # Reconvertir en BGR
        enhanced_lab = cv2.merge([l_channel, a_channel, b_channel])
        result = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        return result

    @staticmethod
    def enhance_saturation(image, strength=1.2):
        """
        Améliore la saturation des couleurs
        
        Args:
            image: Image source
            strength: Force de saturation (1.0-2.0)
            
        Returns:
            Image avec saturation améliorée
        """
        # Convertir en HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h_channel, s_channel, v_channel = cv2.split(hsv)
        
        # Augmenter la saturation
        s_channel = cv2.multiply(s_channel, strength)
        s_channel = np.clip(s_channel, 0, 255).astype(np.uint8)
        
        # Reconvertir en BGR
        enhanced_hsv = cv2.merge([h_channel, s_channel, v_channel])
        result = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)
        
        return result

    @staticmethod
    def apply_all_enhancements(image, upscale=False, denoise=False, sharpen=False, contrast=False, saturation=False):
        """
        Applique tous les filtres d'amélioration à l'image
        
        Args:
            image: Image source
            upscale: Activer l'upscaling 4K
            denoise: Activer le débruitage
            sharpen: Activer l'affinage de netteté
            contrast: Activer l'amélioration du contraste
            saturation: Activer l'amélioration de saturation
            
        Returns:
            Image traitée
        """
        result = image.copy()
        
        if denoise:
            result = ImageEnhancer.denoise(result)
        
        if upscale:
            result = ImageEnhancer.upscale_to_4k(result)
        
        if contrast:
            result = ImageEnhancer.enhance_contrast(result)
        
        if saturation:
            result = ImageEnhancer.enhance_saturation(result)
        
        if sharpen:
            result = ImageEnhancer.enhance_sharpness(result)
        
        return result


class FrameExtractor:
    """Classe pour extraire les frames d'une vidéo"""

    def __init__(self, video_path, output_dir, interval_seconds=1, resize_width=None, resize_height=None, 
                 upscale_4k=False, denoise=False, sharpen=False, enhance_contrast=False, enhance_saturation=False):
        """
        Initialise l'extracteur de frames

        Args:
            video_path: Chemin de la vidéo
            output_dir: Répertoire de sortie
            interval_seconds: Intervalle en secondes entre les frames
            resize_width: Largeur de redimensionnement (optionnel)
            resize_height: Hauteur de redimensionnement (optionnel)
            upscale_4k: Activer l'upscaling en 4K
            denoise: Activer le débruitage
            sharpen: Activer l'affinage de netteté
            enhance_contrast: Activer l'amélioration du contraste
            enhance_saturation: Activer l'amélioration de saturation
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.interval_seconds = interval_seconds
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.upscale_4k = upscale_4k
        self.denoise = denoise
        self.sharpen = sharpen
        self.enhance_contrast = enhance_contrast
        self.enhance_saturation = enhance_saturation
        self.total_frames = 0
        self.processed_frames = 0
        self.is_cancelled = False

    def get_video_info(self):
        """Récupère les informations de la vidéo"""
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                return None

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            cap.release()

            return {
                'fps': fps,
                'total_frames': total_frames,
                'duration': duration,
                'width': width,
                'height': height
            }
        except Exception as e:
            return None

    def extract_frames(self, progress_callback=None):
        """
        Extrait les frames de la vidéo

        Args:
            progress_callback: Fonction de rappel pour la barre de progression
                              Signature: callback(current_frame, total_frames, frame_path)
        """
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise Exception("Impossible d'ouvrir la vidéo")

            # Créer le répertoire de sortie s'il n'existe pas
            os.makedirs(self.output_dir, exist_ok=True)

            fps = cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Calculer le nombre de frames à extraire
            frame_interval = int(fps * self.interval_seconds)
            frame_interval = max(1, frame_interval)  # Au minimum 1

            frame_count = 0
            extracted_count = 0

            while True:
                if self.is_cancelled:
                    break

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    # Redimensionner si nécessaire
                    if self.resize_width or self.resize_height:
                        width = self.resize_width or frame.shape[1]
                        height = self.resize_height or frame.shape[0]
                        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

                    # Appliquer les améliorations d'image
                    if any([self.upscale_4k, self.denoise, self.sharpen, self.enhance_contrast, self.enhance_saturation]):
                        frame = ImageEnhancer.apply_all_enhancements(
                            frame,
                            upscale=self.upscale_4k,
                            denoise=self.denoise,
                            sharpen=self.sharpen,
                            contrast=self.enhance_contrast,
                            saturation=self.enhance_saturation
                        )

                    # Sauvegarder la frame
                    timestamp = int(frame_count / fps)
                    hours = timestamp // 3600
                    minutes = (timestamp % 3600) // 60
                    seconds = timestamp % 60

                    filename = f"frame_{hours:02d}_{minutes:02d}_{seconds:02d}.jpg"
                    filepath = os.path.join(self.output_dir, filename)

                    success = cv2.imwrite(filepath, frame)

                    if success:
                        extracted_count += 1
                        if progress_callback:
                            progress_callback(frame_count, self.total_frames, filepath)

                frame_count += 1

            cap.release()
            return extracted_count

        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction : {str(e)}")

    def cancel(self):
        """Annule l'extraction"""
        self.is_cancelled = True
