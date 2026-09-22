# L3-Lilo UML — Gestion de bibliothèque

Application de gestion de bibliothèque développée en Python, avec interface graphique Qt, gestion des rôles utilisateurs, emprunts, réservations, ressources et catégories.

---

## 🛠️ Technologies utilisées

* **Python** : 3.12 recommandé
* **Python 3.14.x** : supporté selon l'environnement
* **PySide6** : `>=6.6,<7.0`
* **PyQt6** : `>=6.6,<7.0`
* **PyInstaller** : `>=6.0`
* **pip** : gestionnaire de dépendances
* **PlantUML** : diagrammes UML
* **PlantText** : génération et visualisation des diagrammes UML
* **QSS** : personnalisation de l'interface Qt
* **MCP** : outils complémentaires du projet

> **Note Qt :** PySide6 et PyQt6 peuvent cohabiter dans le même environnement tant que les imports ne sont pas mélangés. Le fichier `qt_compat.py` permet d'abstraire la couche Qt utilisée par l'application.

---

## 📦 Installation

### 1. Cloner / récupérer le projet

Depuis la racine du projet :

```text
BIBLIO/
```

### 2. Créer un environnement virtuel

Il est recommandé d'utiliser **Python 3.12**.

Sous Windows :

```powershell
py -3.12 -m venv .venv
```

Activer l'environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

Installation minimale :

```powershell
pip install PySide6
```

Ou, si un fichier `requirements.txt` est présent :

```powershell
pip install -r requirements.txt
```

Les principales dépendances sont :

```text
PySide6>=6.6,<7.0
PyQt6>=6.6,<7.0
pyinstaller>=6.0
```

---

## ▶️ Lancer l'application

Depuis la racine `BIBLIO/` :

```powershell
python -m src.main
```

ou, selon la structure du projet :

```powershell
python main.py
```

---

## 🔐 Connexion

Un compte administrateur est créé automatiquement lorsque la base de données est vide.

### Compte ADMIN par défaut

```text
Email : admin@biblio.local
Mot de passe : admin
```

Il est également possible de cliquer sur **« Accès invité »** afin de tester le mode `GUEST`.

Le rôle `GUEST` possède un accès en lecture seule.

---

# ✨ Fonctionnalités

* ☑ Abstraction PyQt6 / PySide6 via `qt_compat`
* ☑ Thème clair et thème sombre via QSS
* ☑ Changement de thème en un clic
* ☑ Menu latéral avec sélection active
* ☑ Authentification
* ☑ Gestion des rôles `ADMIN`, `SUPERVISEUR` et `GUEST`
* ☑ `MainWindow` avec sidebar
* ☑ Gestion des livres
* ☑ Gestion des usagers
* ☑ Gestion des emprunts
* ☑ Gestion des réservations
* ☑ Gestion des catégories
* ☑ Gestion du personnel
* ☑ Page Livres avec formulaire complet
* ☑ Gestion des images de livres
* ☑ Copie automatique des images dans `datas/`
* ☑ Aperçu des images
* ☑ Gestion des catégories associées aux livres
* ☑ Permissions respectées selon le rôle
* ☑ Affichage des retards en rouge dans la page Emprunts
* ☑ Gestion du stock en temps réel

---

# 📚 Pages de l'application

L'application contient actuellement **6 pages principales** :

1. **Livres**
2. **Usagers**
3. **Emprunts**
4. **Réservations**
5. **Catégories**
6. **Personnel**

---

# ⚙️ Règles métier

Les principales règles métier implémentées sont les suivantes :

| Règle métier                                                    | Implémentation                   |
| --------------------------------------------------------------- | -------------------------------- |
| Un `GUEST` ne peut pas modifier les données                     | `_verifier_ecriture()`           |
| Seul un `ADMIN` peut supprimer                                  | `_verifier_suppression()`        |
| Un même livre ne peut pas être emprunté deux fois simultanément | `creer_emprunt()`                |
| Une réservation prioritaire peut bloquer un emprunt             | `creer_emprunt()`                |
| Le retour d'un livre notifie le prochain réservant              | `_notifier_prochain_reservant()` |
| Une réservation expire automatiquement après 3 jours            | `_rafraichir_reservations()`     |
| Les retards sont détectés automatiquement                       | `_rafraichir_retards()`          |
| Un livre avec un emprunt en cours ne peut pas être supprimé     | `supprimer_livre()`              |
| Un usager avec un emprunt en cours ne peut pas être supprimé    | `supprimer_usager()`             |
| Le stock est décrémenté lors d'une réservation disponible       | `reserver()`                     |

---

# 📊 Gestion du stock

Le stock des livres est géré dynamiquement.

Les opérations sur les livres peuvent modifier la disponibilité en fonction :

* des réservations ;
* des emprunts ;
* des retours ;
* des exemplaires disponibles.

La disponibilité d'un livre peut notamment être déterminée à partir de son stock.

---

# 📐 UML

Les diagrammes UML du projet peuvent être réalisés avec :

* **PlantText**
* **PlantUML**
* l'extension PlantUML de **VS Code**
* l'intégration PlantUML d'un IDE compatible, comme **IntelliJ IDEA**

Les fichiers PlantUML peuvent être conservés dans un dossier dédié :

```text
docs/
└── uml/
    ├── classes.puml
    ├── cas_utilisation.puml
    ├── sequence.puml
    └── workflow.puml
```

---

# 🐛 Bugs connus / fonctionnalités à compléter

### Modification d'un usager

La méthode `modifier_usager` n'est pas encore disponible dans le service.

La modification d'un usager est donc actuellement désactivée.

### `DialogUsager`

Une branche de code fait encore référence à :

```python
self.svc.modifier_livre
```

Cette partie devra être corrigée lorsque la fonctionnalité de modification d'usager sera implémentée.

### Persistance du thème

Le thème sélectionné n'est actuellement pas conservé entre deux lancements de l'application.

Une utilisation de `QSettings` pourrait être ajoutée afin de sauvegarder automatiquement la préférence de l'utilisateur.

### Page Livres

La variable `_item` dans `PageLivres` pourrait être simplifiée.

Il s'agit uniquement d'une amélioration cosmétique / de lisibilité du code.

---

# 🚧 TODO

* [ ] Corriger `modifier_usager`
* [ ] Persister le thème avec `QSettings`
* [ ] Ajouter une fiche détaillée d'un livre

  * image en grand format
  * catégories
  * informations générales
  * historique des emprunts
* [ ] Ajouter une recherche sur les différentes pages
* [ ] Ajouter des filtres sur les listes
* [ ] Ajouter un `build.py`
* [ ] Générer un exécutable avec PyInstaller
* [ ] Tester le build Windows
* [ ] Tester le build Linux / macOS
* [ ] Nettoyer les caches Python avant les builds si nécessaire

---

# 🧹 Dépannage — caches Python

En cas de comportement étrange après une modification du code, il peut être nécessaire de supprimer les dossiers `__pycache__`.

> **Attention :** fermer d'abord l'application et les processus Python qui pourraient utiliser les fichiers.

### 1. Arrêter les processus Python

Depuis PowerShell :

```powershell
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force
```

### 2. Supprimer tous les `__pycache__`

Depuis la racine `BIBLIO/` :

```powershell
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -Force |
    Remove-Item -Recurse -Force
```

### 3. Lancer Python sans générer de `.pyc`

Pour effectuer un test « à blanc » :

```powershell
python -B -m src.main
```

L'option `-B` empêche Python de générer des fichiers `.pyc`.

---

# 🔎 Vérifier ce que Python charge réellement

En cas de problème avec un fichier ou un import, il est possible de vérifier directement son contenu.

Par exemple :

```powershell
python -c "print(repr(open('src/gui/login_window.py','rb').read()[:600]))"
```

Cette commande affiche les premiers octets du fichier réellement lu par Python.

Elle peut être utile pour détecter :

* un mauvais fichier ;
* un ancien fichier ;
* un problème d'encodage ;
* un caractère invisible ;
* un chemin incorrect.

---

# 🐍 Environnement Python recommandé

Pour éviter les problèmes de compatibilité entre versions de Python et bibliothèques Qt, l'environnement recommandé est :

```text
Python 3.12
PySide6
PyQt6
PyInstaller
```

Création de l'environnement :

```powershell
py -3.12 -m venv .venv
```

Activation :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installation :

```powershell
pip install PySide6
```

Lancement :

```powershell
python -m src.main
```

---

# 📁 Fichiers importants

Quelques fichiers importants du projet :

```text
BIBLIO/
│
├── src/
│   ├── main.py
│   ├── core/
│   │   └── services.py
│   │
│   └── gui/
│       └── login_window.py
│
├── datas/
│   └── ...
│
├── requirements.txt
├── qt_compat.py
└── README.md
```

---

# 📝 Notes de développement

Les règles métier principales sont centralisées dans :

```text
core/services.py
```

La compatibilité entre les différentes implémentations Qt est gérée notamment par :

```text
qt_compat.py
```

Les dépendances Python sont listées dans :

```text
requirements.txt
```

Pour une installation reproductible, privilégier :

```powershell
pip install -r requirements.txt
```

---

## 📌 État du projet

Le projet dispose actuellement d'une interface Qt fonctionnelle avec authentification, gestion des rôles, gestion des livres, usagers, emprunts, réservations, catégories et personnel.

Les prochaines étapes concernent principalement la **finalisation de certaines fonctionnalités**, la **persistance des préférences**, la **recherche/filtrage**, ainsi que la **création d'un build distribuable avec PyInstaller**.
