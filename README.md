# Extracteur de Frames Vidéo

Une application Python avec interface graphique (Tkinter) permettant d'extraire les frames d'une vidéo avec plusieurs options de configuration et d'amélioration en 4K.

## Fonctionnalités

✅ **Extraction de frames** - Extrait les frames d'une vidéo à intervalle régulier
✅ **Support multi-formats** - MP4, AVI, MOV
✅ **Intervalle configurable** - Extrait une frame toutes les X secondes
✅ **Redimensionnement optionnel** - Redimensionne les images à la résolution souhaitée
✅ **Barre de progression** - Suivi en temps réel de l'extraction
✅ **Interface intuitive** - Sélection facile des fichiers via Tkinter
✅ **Annulation** - Possibilité d'annuler l'extraction en cours

### Nouvelles Fonctionnalités - Amélioration 4K 🎬

✨ **Upscaling 4K** - Augmente la résolution jusqu'à 3840x2160 (4K) avec haute qualité
✨ **Débruitage avancé** - Réduit le bruit tout en préservant les détails
✨ **Netteté avancée** - Améliore la clarté et la précision des contours
✨ **Amélioration du contraste** - Utilise CLAHE pour un contraste optimal
✨ **Amélioration de saturation** - Augmente la vivacité des couleurs

## Installation

### Prérequis

- Python 3.7+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou installez manuellement :

```bash
pip install opencv-python Pillow
```

## Utilisation

Lancez l'application :

```bash
python app.py
```

### Étapes :

1. **Sélectionnez une vidéo** - Cliquez sur "Parcourir" dans "Vidéo source"
2. **Choisissez un dossier de sortie** - Cliquez sur "Parcourir" dans "Dossier de sortie"
3. **Configurez l'intervalle** - Définissez le nombre de secondes entre les frames
4. **(Optionnel) Redimensionner** - Activez le redimensionnement et entrez la largeur/hauteur
5. **(Optionnel) Améliorations 4K** - Sélectionnez les traitements à appliquer :
   - **Upscale 4K** : Augmente la résolution à 3840x2160
   - **Débruitage** : Réduit le bruit de l'image
   - **Netteté avancée** : Améliore la clarté des détails
   - **Améliorer contraste** : Améliore le contraste avec CLAHE
   - **Améliorer saturation** : Augmente la vivacité des couleurs
6. **Démarrez l'extraction** - Cliquez sur "Démarrer l'extraction"

Les frames seront sauvegardées avec le format de nom : `frame_HH_MM_SS.jpg`

## Structure des fichiers

```
video-frame-extractor/
├── app.py              # Application principale avec interface Tkinter
├── frame_extractor.py  # Classe d'extraction des frames
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

## Détails techniques

### Classe FrameExtractor

- `get_video_info()` - Récupère les informations de la vidéo (FPS, résolution, durée)
- `extract_frames(progress_callback)` - Extrait les frames avec callback de progression
- `cancel()` - Annule l'extraction en cours

### Classe ImageEnhancer

La nouvelle classe `ImageEnhancer` fournit des méthodes statiques pour améliorer les images :

- `upscale_to_4k()` - Upscale les images à 3840x2160 avec interpolation LANCZOS4
- `denoise()` - Applique un débruitage avancé (fastNlMeansDenoising)
- `enhance_sharpness()` - Améliore la netteté avec filtrage convolutif
- `enhance_contrast()` - Améliore le contraste avec CLAHE (Contrast Limited Adaptive Histogram Equalization)
- `enhance_saturation()` - Augmente la saturation des couleurs
- `apply_all_enhancements()` - Applique tous les filtres sélectionnés dans le bon ordre

**Ordre d'application optimal :**
1. Débruitage (réduit le bruit d'abord)
2. Upscaling (augmente la résolution)
3. Amélioration du contraste (améliore la dynamique)
4. Amélioration de saturation (vivacité des couleurs)
5. Affinage de netteté (dernière étape pour maximum de clarté)

### Formats de sortie

Les images extraites sont sauvegardées au format **JPEG** avec le nom suivant :
```
frame_HH_MM_SS.jpg
```

Où `HH`, `MM`, `SS` représentent les heures, minutes et secondes du timestamp.

## Options de redimensionnement

- Largeur ou hauteur seule - L'autre dimension est calculée proportionnellement
- Largeur et hauteur - Les images sont redimensionnées exactement à ces dimensions

## Limitations

- Les vidéos très longues peuvent prendre du temps
- La qualité des images dépend de la vidéo source
- L'extraction se fait en mono-thread
- L'upscaling 4K peut doubler ou tripler le temps de traitement
- Les améliorations 4K augmentent l'utilisation du processeur

## Conseils d'utilisation

### Pour des résultats optimaux :

1. **Vidéos haute résolution** - L'upscaling 4K fonctionne mieux avec des vidéos HD+ (1080p ou plus)
2. **Ordre des filtres** - L'application automatise l'ordre optimal des filtres pour meilleur résultat
3. **Débruitage** - Particulièrement utile pour les vidéos en basse lumière
4. **Netteté avancée** - À combiner avec débruitage pour éviter amplifier le bruit
5. **Saturation** - À utiliser modérément pour éviter des couleurs non naturelles

### Combinaisons recommandées :

- **Photos de meilleure qualité** : Débruitage + Netteté + Contraste
- **Films cinématographiques** : Upscale 4K + Débruitage + Contraste + Saturation
- **Sports/Action** : Upscale 4K + Netteté avancée + Contraste
- **Portraits** : Débruitage + Netteté avancée + Saturation

## Dépannage

### "Impossible d'ouvrir la vidéo"
- Vérifiez que le format vidéo est supporté (MP4, AVI, MOV)
- Assurez-vous que le chemin du fichier ne contient pas de caractères spéciaux
- Vérifiez que OpenCV a accès au fichier

### Espace disque insuffisant
- Les images JPEG non compressées peuvent utiliser beaucoup d'espace
- Utilisez le redimensionnement pour réduire la taille des images

### L'extraction est lente
- Augmentez l'intervalle pour extraire moins de frames
- Activez le redimensionnement pour réduire la taille traitée

## GitHub Pages

GitHub Pages peut héberger une page de documentation statique pour ce projet, mais il ne peut pas exécuter l'application Flask ou le traitement vidéo OpenCV.

- Déployez le dossier `docs/` sur GitHub Pages pour une page de présentation et d'information.
- Pour utiliser l'application, lancez toujours `python app_web.py` localement ou sur un service capable d'exécuter Python (Replit, PythonAnywhere, Heroku, VPS).

## Améliorations futures possibles

- [ ] Multi-threading pour plus de rapidité
- [ ] Compression des images configurable
- [ ] Export en format vidéo
- [ ] Préview des frames extraites
- [ ] Sauvegarde des paramètres

## Licence

MIT
