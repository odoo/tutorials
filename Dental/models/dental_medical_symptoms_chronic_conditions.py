from odoo import fields, models


class ChronicConditions(models.Model):
    _name = 'dental.chronic.conditions'
    _description = 'Chronic Conditions'

    name = fields.Char(string="Name")
    