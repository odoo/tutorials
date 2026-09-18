from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property.tag"
    _description = "Tag of Estate Property"

    name = fields.Char('Nom', required=True)
