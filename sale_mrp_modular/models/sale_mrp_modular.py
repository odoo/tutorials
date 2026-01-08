from odoo import fields, models


class SaleMrpModular(models.Model):
    _name = 'sale.mrp.modular'
    _description = 'List of Modular Types'

    name = fields.Text(string='Modular Type Name')
    color = fields.Integer(string='Color')
