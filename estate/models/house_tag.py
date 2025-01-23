from odoo import fields, models

class house_tag(models.Model):
    _name = 'estate.house_tag'

    name = fields.Char(required=True)
    