from odoo import fields, models


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Medical symptom(Allergies)"
    
    name = fields.Char(required = True)