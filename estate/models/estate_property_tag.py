from odoo import fields, models #type: ignore 


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order = "name"
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.'),
        ]
    _description = 'Property Tag'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
