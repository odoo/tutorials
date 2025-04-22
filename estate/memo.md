# Mémo développement Odoo

- Nommer la branche en : 18.0-feature-rros

- Création de fichier : __init__.py --> fichier de base avec toutes les choses à importer pour la suite de l'exécution
                        __manifest__.py --> fichier contenant les variables relatifs au module

- Génération minimal d'un model :
``` python
from odoo import models

class TestModel(models.Model):
    _name = "test_model"
```
- Sécurité : dans le dossier security, le fichier `ir.model.access.csv` permet de définir les différents niveaux d'accès

- 
