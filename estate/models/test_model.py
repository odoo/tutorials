from odoo import models, fields

class MyModel(models.Model):
    _name = 'test_model'
    _description = 'My New Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text()
    address = fields.Text()