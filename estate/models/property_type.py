from odoo import models, fields


class EstateTypeModel(models.Model):
    _name = 'estate.type'
    _description = "Real estate types model"

    type = fields.Char()

    _sql_constraints = [
        ('unique_type', 'UNIQUE(type)',
         'Expected type to be unique'),
    ]
