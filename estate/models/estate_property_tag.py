from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Specific tags for properties"
    _order = "name desc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer('color')
    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tag already created')
    ]
