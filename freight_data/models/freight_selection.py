from odoo import fields, models


class FreightSelection(models.Model):
    _name = 'freight.selection'
    _description = 'Freight Selection Options'

    name = fields.Char(required=True, string="Freight Option")
