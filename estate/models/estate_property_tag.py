from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(
        string='Color', help="Color used in the Kanban view")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'THE PROPERTY TAG NAME MUST BE UNIQUE ! ...')
    ]
