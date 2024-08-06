from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This property type already exists.'),
    ]
