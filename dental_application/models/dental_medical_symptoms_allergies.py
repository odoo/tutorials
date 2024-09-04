from odoo import models, fields


class Allergies(models.Model):
    _name = 'dental.allergies'
    _description = 'Allergies'

    name = fields.Char(string="Name")
