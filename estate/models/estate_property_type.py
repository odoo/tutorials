from odoo import models, fields

class EstatePropertyType(models.Model):
    
    _name = "estate_property.type"
    _description = "Types of Estate Property"

    name = fields.Char('Nom', required=True)

    