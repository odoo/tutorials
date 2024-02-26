from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag model"
    _order = "name"


    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'Tag name should be unique')
    ]
