from odoo import models,fields

class TestPropertyType(models.Model):
    _name = "test.property.type"

    name = fields.Char('name')
    description=fields.Char('description')
