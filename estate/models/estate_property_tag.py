from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'THE PROPERTY TAG NAME MUST BE UNIQUE ! ...')
    ]
