from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    receipt_layout = fields.Selection(
        [("light", "Light"), ("boxes", "Boxes"), ("lined", "Lined")],
        string="Select Layout",
        default="light",
    )
    receipt_logo = fields.Binary(
        string="Company Logo",
        related="company_id.logo",
        readonly=False,
        help="A logo that will be printed in the receipt.",
    )
