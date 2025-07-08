from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Estate property "
    _order = "name asc"

    name = fields.Char(required=True, string='Name')
    color = fields.Integer(default=3)



    _sql_constraints=[
        ('unique_property_tag_name', 'UNIQUE(name)', 'A property tag name must be unique.'),
    ]