# Mémo développement Odoo

- Nommer la branche en : 18.0-feature-rros

- Création de fichier : __init__.py --> fichier de base avec toutes les choses à importer pour la suite de l'exécution
                        __manifest__.py --> fichier contenant les variables relatifs au module

| Attention, bien ajouter le fichier du modèle dans le __init__.py du répertoire courant au fichier
- Génération minimal d'un model :
``` python
from odoo import models

class TestModel(models.Model):
    _name = "test_model"
```
- Sécurité : dans le dossier security, le fichier `ir.model.access.csv` permet de définir les différents niveaux d'accès

- Pour lier un bouton à une action : `ir.actions.act_window` dans le .xml
- Pour lier un vue à un modèle : `ir.ui.view` dans le .xml

- Calcul de valeur avec `compute` (appelée à chaque modification d'une valeur des dépendances):
``` python
    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount
```
- Calcul de valeur avec `inverse` (appelée à chaque sauvegarde de l'enregistrement):
``` python
    def _inverse_total(self):
        for record in self:
            record.amount = record.total / 2.0
```