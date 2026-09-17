from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Estate Property"

    name = fields.Char('Nom', required=True)