from odoo import fields, models

class house_type(models.Model):
    _name = 'estate.house_type'

    name = fields.Char(required=True)
