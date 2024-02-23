from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    _sql_constraints = (
        ('unique_name', 'UNIQUE(name)',
         'Tag name should be unique'),
    )

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()
