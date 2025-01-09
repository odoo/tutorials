from odoo import models,fields
from random import randint

class TestPropertyTags(models.Model):
    _name = "test.property.tags"
    _description = "Test proerty Tags"
    _order = "name"

    name = fields.Char('name')
    color = fields.Integer(
        'Color',
        default=lambda self : self._default_color()
    )


    def _default_color(self):
        return randint(1, 11)