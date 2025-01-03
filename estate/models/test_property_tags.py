from odoo import models,fields

class TestPropertyTags(models.Model):
    _name = "test.property.tags"

    name = fields.Char('name')
