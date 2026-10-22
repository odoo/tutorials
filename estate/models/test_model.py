
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model for Tutorials"

    name = fields.Char()
