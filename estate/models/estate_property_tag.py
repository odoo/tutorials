from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char(required=True, string="Name")
    color = fields.Integer()
    
    _sql_constraints = [
        ('check_expected_price', 'UNIQUE (name)', 'A property tag name must be unique'),
    ]
