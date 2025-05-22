from odoo import fields, models


class TestModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Model Tag'

    name = fields.Char(required=True)
