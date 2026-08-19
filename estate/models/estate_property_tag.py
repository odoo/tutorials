from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Tag Name", required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Tag name must be unique.'
    )
