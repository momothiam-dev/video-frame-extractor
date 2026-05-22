#!/usr/bin/env python3
"""
Version web Flask - Video Frame Extractor 4K
Déploiement sur téléphone et navigateur
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import threading
from frame_extractor import FrameExtractor
import json
from pathlib import Path
import zipfile
import shutil

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'extracted_frames'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max

# Variables globales
extraction_status = {
    'progress': 0,
    'status': 'idle',
    'message': '',
    'total_frames': 0,
    'current_frame': 0
}
current_extractor = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html')


@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """Récupère les infos de la vidéo uploadée"""
    try:
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier sélectionné'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Fichier vide'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': f'Format non supporté. Formats autorisés: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Créer dossier uploads s'il n'existe pas
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Sauvegarder le fichier
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
        except Exception as save_err:
            return jsonify({'success': False, 'error': f'Erreur sauvegarde: {str(save_err)}'}), 500
        
        # Vérifier que le fichier existe
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Fichier non sauvegardé correctement'}), 500
        
        # Récupérer les infos
        try:
            extractor = FrameExtractor(filepath, app.config['UPLOAD_FOLDER'])
            info = extractor.get_video_info()
        except Exception as cv_err:
            return jsonify({'success': False, 'error': f'Erreur OpenCV: {str(cv_err)}'}), 500
        
        if info:
            return jsonify({
                'success': True,
                'filename': filename,
                'resolution': f"{info['width']}x{info['height']}",
                'fps': f"{info['fps']:.2f}",
                'duration': int(info['duration']),
                'total_frames': info['total_frames']
            })
        else:
            return jsonify({'success': False, 'error': 'Impossible de lire la vidéo. Vérifiez le format et la taille'}), 400
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'success': False, 'error': f'Erreur: {str(e)}', 'details': error_details}), 500


@app.route('/api/extract', methods=['POST'])
def extract_frames():
    """Démarre l'extraction des frames"""
    global current_extractor, extraction_status
    
    try:
        data = request.json
        video_filename = data.get('filename')
        interval = float(data.get('interval', 1))
        upscale_4k = data.get('upscale_4k', False)
        denoise = data.get('denoise', False)
        sharpen = data.get('sharpen', False)
        contrast = data.get('contrast', False)
        saturation = data.get('saturation', False)
        
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        
        if not os.path.exists(video_path):
            return jsonify({'error': 'Vidéo non trouvée'}), 404
        
        # Créer dossier de sortie
        output_dir = os.path.join(OUTPUT_FOLDER, Path(video_filename).stem)
        os.makedirs(output_dir, exist_ok=True)
        
        # Réinitialiser le statut
        extraction_status = {
            'progress': 0,
            'status': 'extracting',
            'message': 'Extraction en cours...',
            'total_frames': 0,
            'current_frame': 0
        }
        
        # Créer l'extracteur
        current_extractor = FrameExtractor(
            video_path,
            output_dir,
            interval,
            upscale_4k=upscale_4k,
            denoise=denoise,
            sharpen=sharpen,
            enhance_contrast=contrast,
            enhance_saturation=saturation
        )
        
        # Lancer extraction dans un thread
        def run_extraction():
            global extraction_status
            try:
                def progress_callback(current, total, path):
                    global extraction_status
                    extraction_status['current_frame'] = current
                    extraction_status['total_frames'] = total
                    extraction_status['progress'] = int((current / total) * 100) if total > 0 else 0
                
                count = current_extractor.extract_frames(progress_callback)
                extraction_status['status'] = 'completed'
                extraction_status['message'] = f'{count} frames extraites avec succès!'
                extraction_status['progress'] = 100
                
            except Exception as e:
                extraction_status['status'] = 'error'
                extraction_status['message'] = f'Erreur: {str(e)}'
        
        thread = threading.Thread(target=run_extraction)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Extraction démarrée'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def get_status():
    """Récupère le statut de l'extraction"""
    return jsonify(extraction_status)


@app.route('/api/cancel', methods=['POST'])
def cancel_extraction():
    """Annule l'extraction"""
    global current_extractor, extraction_status
    
    if current_extractor:
        current_extractor.cancel()
        extraction_status['status'] = 'cancelled'
        extraction_status['message'] = 'Extraction annulée'
    
    return jsonify({'success': True})


@app.route('/api/download-frames')
def download_frames():
    """Télécharge les frames extraites en ZIP"""
    try:
        output_dir = OUTPUT_FOLDER
        
        if not os.path.exists(output_dir) or not os.listdir(output_dir):
            return jsonify({'error': 'Aucune frame extraite'}), 404
        
        # Créer un ZIP
        zip_path = 'extracted_frames.zip'
        shutil.make_archive('extracted_frames', 'zip', output_dir)
        
        return send_file(zip_path, as_attachment=True, download_name='frames.zip')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_data():
    """Efface les fichiers temporaires"""
    try:
        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        return jsonify({'success': True, 'message': 'Données effacées'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    # Déployer sur tous les interfaces réseau
    app.run(host='0.0.0.0', port=port, debug=debug)
