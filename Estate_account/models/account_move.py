from odoo import models, fields


class EstateMove(models.Model):
    _inherit = "account.move"

    property_id = fields.Char()
