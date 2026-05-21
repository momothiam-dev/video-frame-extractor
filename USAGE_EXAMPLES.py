#!/usr/bin/env python3
"""
Guide d'utilisation - Amélioration d'image 4K
Exemples d'utilisation de la classe ImageEnhancer
"""

from frame_extractor import FrameExtractor, ImageEnhancer
import cv2


# ============================================================================
# EXEMPLE 1: Extraction simple sans améliorations
# ============================================================================
def example_basic_extraction():
    """Extraction basique de frames"""
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames_output",
        interval_seconds=1.0
    )
    
    # Extraire les frames
    count = extractor.extract_frames()
    print(f"✓ {count} frames extraites")


# ============================================================================
# EXEMPLE 2: Extraction avec upscale 4K uniquement
# ============================================================================
def example_4k_upscale():
    """Extraction avec upscale en 4K"""
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames_4k",
        interval_seconds=1.0,
        upscale_4k=True  # Activer upscale 4K
    )
    
    count = extractor.extract_frames()
    print(f"✓ {count} frames en 4K extraites")


# ============================================================================
# EXEMPLE 3: Extraction avec tous les filtres de qualité
# ============================================================================
def example_full_enhancement():
    """Extraction avec amélioration complète"""
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames_enhanced",
        interval_seconds=1.0,
        upscale_4k=True,          # Upscale 4K
        denoise=True,              # Débruitage
        sharpen=True,              # Netteté
        enhance_contrast=True,     # Contraste
        enhance_saturation=True    # Saturation
    )
    
    count = extractor.extract_frames()
    print(f"✓ {count} frames avec amélioration complète extraites")


# ============================================================================
# EXEMPLE 4: Extraction avec amélioration ciblée (films)
# ============================================================================
def example_cinematic_quality():
    """Extraction avec qualité cinématographique"""
    extractor = FrameExtractor(
        video_path="mon_film.mp4",
        output_dir="frames_cinema",
        interval_seconds=0.5,  # Plus de frames
        upscale_4k=True,       # Résolution maximale
        denoise=True,          # Réduire bruit
        enhance_contrast=True, # Améliorer dynamique
        enhance_saturation=True  # Couleurs vivantes
    )
    
    count = extractor.extract_frames()
    print(f"✓ {count} frames de qualité cinéma extraites")


# ============================================================================
# EXEMPLE 5: Utilisation directe de ImageEnhancer
# ============================================================================
def example_direct_enhancement():
    """Amélioration directe d'une image"""
    # Charger une image
    image = cv2.imread("ma_photo.jpg")
    
    # Option 1: Appliquer chaque filtre individuellement
    denoised = ImageEnhancer.denoise(image)
    sharpened = ImageEnhancer.enhance_sharpness(denoised)
    
    # Option 2: Appliquer tous les filtres d'un coup
    enhanced = ImageEnhancer.apply_all_enhancements(
        image,
        upscale=True,
        denoise=True,
        sharpen=True,
        contrast=True,
        saturation=True
    )
    
    # Sauvegarder
    cv2.imwrite("ma_photo_enhanced.jpg", enhanced)
    print(f"✓ Image améliorée sauvegardée")


# ============================================================================
# EXEMPLE 6: Traitement par lot avec progression
# ============================================================================
def example_batch_processing_with_progress():
    """Traitement avec callback de progression"""
    
    def progress_callback(current_frame, total_frames, frame_path):
        progress = int((current_frame / total_frames) * 100)
        print(f"Progression: {progress}% - {frame_path}")
    
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames_batch",
        interval_seconds=2.0,
        upscale_4k=True,
        denoise=True,
        sharpen=True
    )
    
    count = extractor.extract_frames(progress_callback=progress_callback)
    print(f"✓ Extraction terminée: {count} frames")


# ============================================================================
# EXEMPLE 7: Extraction avec annulation
# ============================================================================
def example_extraction_with_cancellation():
    """Extraction avec possibilité d'annulation"""
    import threading
    import time
    
    extractor = FrameExtractor(
        video_path="long_video.mp4",
        output_dir="frames_cancellable",
        interval_seconds=1.0,
        upscale_4k=True
    )
    
    # Démarrer extraction dans un thread
    extraction_thread = threading.Thread(
        target=extractor.extract_frames
    )
    extraction_thread.start()
    
    # Attendre 10 secondes puis annuler
    time.sleep(10)
    extractor.cancel()
    
    extraction_thread.join()
    print("✓ Extraction annulée")


# ============================================================================
# EXEMPLE 8: Informations vidéo avant extraction
# ============================================================================
def example_video_info():
    """Récupérer les informations vidéo"""
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames"
    )
    
    info = extractor.get_video_info()
    
    if info:
        print(f"Résolution: {info['width']}x{info['height']}")
        print(f"FPS: {info['fps']}")
        print(f"Durée: {info['duration']} secondes")
        print(f"Total frames: {info['total_frames']}")
    else:
        print("❌ Impossible de lire la vidéo")


# ============================================================================
# EXEMPLE 9: Redimensionnement + Amélioration
# ============================================================================
def example_resize_and_enhance():
    """Redimensionner puis améliorer"""
    extractor = FrameExtractor(
        video_path="mon_video.mp4",
        output_dir="frames_optimized",
        interval_seconds=1.0,
        resize_width=1920,      # Redimensionner à 1920x1080
        resize_height=1080,
        upscale_4k=False,       # Ne pas upscaler après redimensionnement
        denoise=True,
        sharpen=True,
        enhance_contrast=True
    )
    
    count = extractor.extract_frames()
    print(f"✓ {count} frames redimensionnées et améliorées")


# ============================================================================
# EXEMPLE 10: Configuration recommandée par type de contenu
# ============================================================================

def get_extractor_for_content_type(video_path, content_type):
    """Retourner une configuration optimale selon le type"""
    
    configs = {
        "cinema": {
            "upscale_4k": True,
            "denoise": True,
            "sharpen": False,
            "enhance_contrast": True,
            "enhance_saturation": True,
            "interval": 0.5
        },
        "sport": {
            "upscale_4k": True,
            "denoise": False,
            "sharpen": True,
            "enhance_contrast": True,
            "enhance_saturation": False,
            "interval": 0.25
        },
        "portrait": {
            "upscale_4k": False,
            "denoise": True,
            "sharpen": True,
            "enhance_contrast": False,
            "enhance_saturation": True,
            "interval": 2.0
        },
        "nature": {
            "upscale_4k": True,
            "denoise": True,
            "sharpen": False,
            "enhance_contrast": True,
            "enhance_saturation": True,
            "interval": 1.0
        }
    }
    
    config = configs.get(content_type, configs["cinema"])
    
    return FrameExtractor(
        video_path=video_path,
        output_dir=f"frames_{content_type}",
        interval_seconds=config["interval"],
        upscale_4k=config["upscale_4k"],
        denoise=config["denoise"],
        sharpen=config["sharpen"],
        enhance_contrast=config["enhance_contrast"],
        enhance_saturation=config["enhance_saturation"]
    )


# ============================================================================
# UTILISATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Exemples d'utilisation - Video Frame Extractor 4K")
    print("=" * 60)
    print()
    print("Décommentez l'exemple que vous souhaitez exécuter:")
    print()
    
    # Choisir un exemple et le décommenter
    # example_basic_extraction()
    # example_4k_upscale()
    # example_full_enhancement()
    # example_cinematic_quality()
    # example_direct_enhancement()
    # example_batch_processing_with_progress()
    # example_extraction_with_cancellation()
    # example_video_info()
    # example_resize_and_enhance()
    
    # Exemple avec type de contenu
    # extractor = get_extractor_for_content_type("mon_video.mp4", "cinema")
    # extractor.extract_frames()
    
    print("✓ Exemples disponibles - À adapter à votre besoin")
