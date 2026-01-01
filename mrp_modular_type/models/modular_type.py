from odoo import fields, models


class ModularType(models.Model):
    _name = 'modular.type'

    name = fields.Char(string="Modular Type Name", required=True)
    qty_multiplier = fields.Integer(string="Quantity Multiplier", default=0)

    _sql_constraints = [
        ('quantity_multiplier_check', 'CHECK(qty_multiplier > 0)', "Quantity Multiplier must be greater than 0")
    ]
