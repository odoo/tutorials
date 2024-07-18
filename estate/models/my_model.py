# models/my_model.py
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'My.model'
    _description = 'My Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    @api.model
    def create_record(self, values):
        pass