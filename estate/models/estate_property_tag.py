from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Table for tags of a property"

    name = fields.Char(required=True)
    _check_name = models.Constraint("UNIQUE(name)", "Le nom du tag doit être unique")
