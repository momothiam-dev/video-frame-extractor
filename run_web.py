#!/usr/bin/env python3
"""
Script de lancement - Version Web Mobile
Lance le serveur Flask sur 0.0.0.0:5000
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au chemin
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == '__main__':
    import socket
    import webbrowser
    from app_web import app
    
    # Récupérer l'adresse IP locale
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*60)
    print("🚀 SERVEUR WEB - Video Frame Extractor 4K")
    print("="*60)
    print()
    print(f"✓ Serveur démarrant sur port {port}...")
    print()
    print(f"📱 Accès LOCAL   : http://localhost:{port}")
    print(f"🌐 Accès RÉSEAU  : http://{ip}:{port}")
    print()
    print("Sur téléphone (même réseau):")
    print(f"  → Ouvrez: http://{ip}:{port}")
    print()
    print("Appuyez sur CTRL+C pour arrêter")
    print("="*60 + "\n")
    
    # Tenter ouverture du navigateur
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    # Démarrer le serveur
    app.run(host='0.0.0.0', port=port, debug=False)
