from odoo import fields, models


class AccounMoves(models.Model):
    _inherit = "account.move"

    property_name = fields.Char()
