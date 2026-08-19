from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Tag name must be unique.'
    )
