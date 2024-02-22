from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = (
        ('unique_name', 'UNIQUE(name)',
         'Tag name should be unique'),
    )

    _order = "name"

    color = fields.Integer()
