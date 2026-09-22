# L3-Lilo UML Gestion de bibliothèque

# Python 3.14.5
# Python 3.14
# Python 3.12

# pyQT 6
# pyside 6

# pip

Bootstrap

compilable, avec mcp

PlantText ou l'éditeur PlantUML de ton IDE (VS Code, IntelliJ, etc.)

temps reel pour le stock

PlantText ou l'éditeur PlantUML de ton IDE (VS Code, IntelliJ, etc.)

PySide6>=6.6,<7.0
PyQt6>=6.6,<7.0
pyinstaller>=6.0
Note : les deux peuvent cohabiter sans souci tant qu'on ne mélange pas les imports. Notre qt_compat.py gère ça.


Règles métier implémentées
Règle	Où
GUEST ne peut pas modifier	_verifier_ecriture()
Seul ADMIN supprime	_verifier_suppression()
Pas de double emprunt du même livre	creer_emprunt
Réservation prioritaire bloque l'emprunt	creer_emprunt
Retour → notifie le prochain réservant	_notifier_prochain_reservant
Expiration auto réservation (3 j)	_rafraichir_reservations
Retard auto-détecté	_rafraichir_retards
Suppression bloquée si emprunt en cours	supprimer_livre, supprimer_usager
Stock décrémenté à la réservation DISPONIBLE	reserver

# Installer les dépendances
pip install PySide6

# Lancer
python main.py


Connexion par défaut (créée automatiquement si la base est vide) :

Email : admin@biblio.local

Mot de passe : admin

Ou clique sur "Accès invité" pour tester le mode GUEST (lecture seule).


✅ Features
☑ Abstraction PyQt6 / PySide6 (qt_compat)
☑ Thèmes clair + sombre via QSS, commutable en 1 clic
☑ Menu latéral avec sélection active
☑ Login (ADMIN/SUPERVISEUR + invité)
☑ MainWindow avec sidebar
☑ 6 pages : Livres, Usagers, Emprunts, Réservations, Catégories, Personnel
☑ Page Livres avec formulaire complet (image + catégories + aperçu + placeholder)
☑ Sélecteur d'image avec copie auto dans datas/
☑ Permissions respectées (boutons masqués selon le rôle)
☑ Retards colorés en rouge dans Emprunts

🐛 Bugs connus / à compléter
modifier_usager n'existe pas encore dans le service — la modification d'usager est désactivée. Dis-moi si tu veux que je l'ajoute.

DialogUsager : j'ai laissé une branche morte (self.svc.modifier_livre). À corriger dès qu'on ajoute la vraie modif.

Persistance du thème entre lancements : pas encore géré (pas de QSettings). À ajouter si tu veux.

Le _item dans PageLivres pourrait être simplifié — c'est cosmétique.

➡️ TODO
Corriger modifier_usager (2 min)

Persister le thème via QSettings (2 min)

Écran de détail d'un livre (double-clic → fiche complète avec image grande, catégories, historique emprunts)

Recherche / filtre en haut de chaque page

build.py avec PyInstaller → .exe (Windows) / binaire (Linux/Mac)

pour debug caches


Fix immédiat
Depuis la racine BIBLIO/, supprime tous les __pycache__ :

Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

Fix immédiat
Depuis BIBLIO/, supprime tous les __pycache__ (tue d'abord tout Python qui pourrait les verrouiller) :

Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force

puis

Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -Force | Remove-Item -Recurse -Force

puis

Puis relance avec -B pour empêcher Python de régénérer un cache (test à blanc) :

python -B -m src.main

commande pour voir ce que Python lit vraiment dans ce fichier au moment de l'import :

python -c "print(repr(open('src/gui/login_window.py','rb').read()[:600]))"


venv propre avec Python 3.12 (recommandé) :
# Installe Python 3.12 si tu ne l'as pas
# Puis dans BIBLIO/ :
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install PySide6
python -m src.main


Solution : utiliser explicitement Python 3.12
Depuis BIBLIO/, crée un venv avec le bon Python :


Notes:

src/servives.py
requirements.txt
