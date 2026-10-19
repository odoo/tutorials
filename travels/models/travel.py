from odoo import fields, models


class Travel(models.TransientModel):
    _name = "yash.travels"
    _description = "Yash Travels"
    # _transient_max_hours = 0.01
    _transient_max_count = 1
    name = fields.Char(required=True)
    destination = fields.Char()
    amount = fields.Float()
