from odoo import fields, models


class TestModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Model Type'

    name = fields.Char(required=True)
