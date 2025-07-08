from odoo import  fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of estate are defined"

    name = fields.Char(required = True)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', 'The name of the tag should be unique')
    ]

    _order = "name asc"

    color = fields.Integer()