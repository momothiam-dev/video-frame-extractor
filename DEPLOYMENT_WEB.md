# 📱 Guide de Déploiement - Version Web Mobile

## ✨ Nouvelles Fonctionnalités

✅ **Interface Web Responsive** - Fonctionne sur Téléphone, Tablette, Desktop
✅ **Accès Local** - Via navigateur sur le même réseau
✅ **Téléchargement de Frames** - ZIP des images extraites
✅ **Design Mobile-First** - Interface optimisée tactile

---

## 🚀 Démarrage Rapide

### 1. **Lancer le serveur web**

```bash
python app_web.py
```

Le serveur démarre sur `http://localhost:5000` ou `http://0.0.0.0:5000`

**Output attendu :**
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### 2. **Accéder depuis le navigateur**

#### Sur le même PC:
- Ouvrez: `http://localhost:5000`

#### Sur téléphone/autre PC (même réseau):
1. Trouvez l'adresse IP de votre PC (Windows):
   ```bash
   ipconfig
   ```
   Cherchez la ligne `IPv4 Address` (ex: `192.168.1.100`)

2. Sur votre téléphone/autre PC, ouvrez:
   ```
   http://192.168.1.100:5000
   ```

---

## 📱 Utilisation sur Téléphone

### **iOS Safari / Android Chrome:**

1. ✅ Ouvrez le navigateur
2. ✅ Saisissez l'adresse web
3. ✅ **Sélectionnez une vidéo** (glissez-déposez ou clic)
4. ✅ **Configurez les paramètres**
5. ✅ **Activez les améliorations 4K** (optionnel)
6. ✅ **Démarrez l'extraction**
7. ✅ **Téléchargez les frames en ZIP**

---

## 🌐 Déploiement en Production

### **Option 1: Heroku (Gratuit + Payant)**

```bash
# Installer Heroku CLI
# Créer app.py compatible
pip install gunicorn

# Heroku Procfile
echo "web: gunicorn app_web:app" > Procfile

# Deploy
heroku create
git push heroku main
```

### **Option 2: PythonAnywhere**

1. Créer compte gratuit: https://www.pythonanywhere.com
2. Uploader les fichiers
3. Configurer l'application Flask
4. Lien public généré automatiquement

### **Option 3: AWS/Azure**

```bash
# AWS EC2 ou Azure App Service
# Lancer serveur sur port 80/443
gunicorn --bind 0.0.0.0:80 app_web:app
```

### **Option 4: Google Cloud / Replit**

Déploiement instant avec interface graphique.

---

## 🔧 Configuration Avancée

### **Changer le port:**

```bash
# Éditer app_web.py (ligne finale)
# app.run(host='0.0.0.0', port=8000)  # Port 8000
```

### **Activer HTTPS (Production):**

```bash
pip install flask-talisman
# Ajouter SSL certificate
```

### **Augmenter limite fichiers:**

```python
# app_web.py
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024  # 2GB
```

---

## 📊 Fichiers Créés

```
video-frame-extractor/
├── app_web.py              # Serveur Flask
├── templates/
│   └── index.html          # Interface Web Responsive
├── uploads/                # Dossier temporaire (vidéos)
├── extracted_frames/       # Dossier temporaire (frames)
└── requirements.txt        # Dépendances mises à jour
```

---

## ⚡ Performance

- Upload vidéo: ~100MB/sec
- Extraction: Dépend de la vidéo
- Téléchargement ZIP: Rapide (streaming)
- Mémoire: ~500MB pour operation normale

---

## 🐛 Dépannage

### "Connexion refusée"
```bash
# Vérifier que le serveur tourne
# Vérifier l'adresse IP/port
# Vérifier le firewall
```

### "Fichier trop volumineux"
```bash
# Augmenter la limite dans app_web.py
# Ou réduire la vidéo avant upload
```

### "Extraction très lente"
```bash
# Réduire l'intervalle (ex: 2 au lieu de 1)
# Désactiver les améliorations 4K
# Utiliser vidéo plus petite
```

---

## 🎯 Prochaines Étapes

- [ ] Ajouter authentification utilisateur
- [ ] Base de données pour historique
- [ ] Support multi-utilisateurs simultanés
- [ ] API REST complète
- [ ] App mobile native (React Native)
- [ ] Websockets pour temps réel

---

## 📚 Commandes Utiles

```bash
# Lancer serveur web
python app_web.py

# Lancer sur port spécifique
python -c "
import app_web
app_web.app.run(host='0.0.0.0', port=8080)
"

# Vérifier adresse IP
ipconfig

# Tester connexion
curl http://localhost:5000
```

---

**✅ Version Web Déployée et Prête à l'Emploi !** 🚀
