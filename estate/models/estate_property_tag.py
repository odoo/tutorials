from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = 'name'

    color = fields.Integer()
    name = fields.Char(required=True)

    _sql_constraints =[
        ('_unique_name','UNIQUE(name)','Tags must be unique'),
    ]
