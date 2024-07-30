from odoo import fields, models


class FreightIsOptions(models.Model):
    _name = "freight.is.options"
    _description = "Freight Is Options Model"

    name = fields.Char()
