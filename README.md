# Widget post-it de dosimétrie

Ce dépôt contient un petit widget Python (Tkinter) pensé pour la planification de traitement en dosimétrie.

## Fonctionnalités
- Fenêtre compacte type **post-it**, toujours au premier plan.
- Saisie du **nombre de niveaux de dose**.
- Saisie de la **prescription de chaque niveau** (en Gy).
- Calcul automatique, pour chaque niveau, des valeurs à : **10%, 50%, 95%, 98%, 100%, 105% et 107%**.

## Lancer le widget
Prérequis : Python 3 (Tkinter est généralement inclus par défaut).

```bash
python3 widgets/widget_dosimetrie.py
```

Le widget restera affiché sur l'écran pour un usage rapide pendant la planification.
