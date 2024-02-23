from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag model"


    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'Tag name should be unique')
    ]
