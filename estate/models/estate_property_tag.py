from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "used to add precision to a property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The name of a tag should be unique'),
    ]
