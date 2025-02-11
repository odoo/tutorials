from odoo import fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'stores property tags'
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_property_tag_name', 'UNIQUE(name)', 'Property Tag name must be unique')
    ]
