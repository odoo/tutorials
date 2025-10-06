from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    simplified_receipt = fields.Boolean(
        string="Simplified receipts",
        help="Print Receipt with no details about the items bought",
    )
