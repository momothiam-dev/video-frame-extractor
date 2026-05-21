#!/usr/bin/env python3
"""
Script de test pour les fonctionnalités d'amélioration 4K
Démontre l'utilisation de la classe ImageEnhancer
"""

import cv2
import numpy as np
from frame_extractor import ImageEnhancer
import os


def create_test_image():
    """Crée une image de test simple"""
    # Créer une image 800x600
    image = np.ones((600, 800, 3), dtype=np.uint8) * 100
    
    # Ajouter du bruit
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)
    
    # Ajouter un gradient
    for y in range(image.shape[0]):
        image[y, :] = image[y, :].astype(int) + int(y / 3)
    
    image = np.clip(image, 0, 255).astype(np.uint8)
    
    # Ajouter du texte
    cv2.putText(image, "Test Image", (250, 300), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 255, 255), 3)
    cv2.circle(image, (400, 300), 100, (0, 255, 0), -1)
    
    return image


def test_enhancements():
    """Test toutes les fonctionnalités d'amélioration"""
    
    print("=" * 60)
    print("TEST - Fonctionnalités d'Amélioration d'Image 4K")
    print("=" * 60)
    
    # Créer l'image de test
    image = create_test_image()
    print(f"\n✓ Image de test créée: {image.shape}")
    
    # Créer le dossier de sortie
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Sauvegarder l'image originale
    cv2.imwrite(os.path.join(output_dir, "01_original.jpg"), image)
    print("✓ Image originale sauvegardée: 01_original.jpg")
    
    # Test Upscaling 4K
    print("\n▶ Test Upscaling 4K...")
    upscaled = ImageEnhancer.upscale_to_4k(image, 3840, 2160)
    cv2.imwrite(os.path.join(output_dir, "02_upscaled_4k.jpg"), upscaled)
    print(f"✓ Image upscalée: {upscaled.shape}")
    
    # Test Débruitage
    print("\n▶ Test Débruitage...")
    denoised = ImageEnhancer.denoise(image, strength=10)
    cv2.imwrite(os.path.join(output_dir, "03_denoised.jpg"), denoised)
    print(f"✓ Image débruitée: {denoised.shape}")
    
    # Test Netteté avancée
    print("\n▶ Test Netteté avancée...")
    sharpened = ImageEnhancer.enhance_sharpness(image, strength=1.5)
    cv2.imwrite(os.path.join(output_dir, "04_sharpened.jpg"), sharpened)
    print(f"✓ Image affinée: {sharpened.shape}")
    
    # Test Amélioration du contraste
    print("\n▶ Test Amélioration du contraste...")
    contrast_enhanced = ImageEnhancer.enhance_contrast(image, strength=1.2)
    cv2.imwrite(os.path.join(output_dir, "05_contrast_enhanced.jpg"), contrast_enhanced)
    print(f"✓ Image avec contraste amélioré: {contrast_enhanced.shape}")
    
    # Test Amélioration de saturation
    print("\n▶ Test Amélioration de saturation...")
    saturation_enhanced = ImageEnhancer.enhance_saturation(image, strength=1.3)
    cv2.imwrite(os.path.join(output_dir, "06_saturation_enhanced.jpg"), saturation_enhanced)
    print(f"✓ Image avec saturation améliorée: {saturation_enhanced.shape}")
    
    # Test Application de tous les filtres
    print("\n▶ Test Application de tous les filtres...")
    all_enhanced = ImageEnhancer.apply_all_enhancements(
        image,
        upscale=True,
        denoise=True,
        sharpen=True,
        contrast=True,
        saturation=True
    )
    cv2.imwrite(os.path.join(output_dir, "07_all_enhancements.jpg"), all_enhanced)
    print(f"✓ Image avec tous les filtres: {all_enhanced.shape}")
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"\n✓ Tous les tests ont réussi!")
    print(f"✓ Les images de test ont été sauvegardées dans: {output_dir}/")
    print("\nFichiers générés:")
    print("  - 01_original.jpg           : Image originale")
    print("  - 02_upscaled_4k.jpg        : Upscale 4K")
    print("  - 03_denoised.jpg           : Débruitage")
    print("  - 04_sharpened.jpg          : Netteté avancée")
    print("  - 05_contrast_enhanced.jpg  : Contraste amélioré")
    print("  - 06_saturation_enhanced.jpg: Saturation améliorée")
    print("  - 07_all_enhancements.jpg   : Tous les filtres appliqués")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_enhancements()
