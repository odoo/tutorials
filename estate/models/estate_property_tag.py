from odoo import fields, models


class TestModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Model Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
