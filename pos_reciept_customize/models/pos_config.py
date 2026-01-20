# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    receipt_layout = fields.Selection([
        ("light", "Light"),
        ("boxes", "Boxes"),
        ("lined", "Lined")],
        string="Receipt Layout",
        default="light",
    )
    receipt_logo = fields.Binary(related="company_id.logo", string="Receipt Logo")
    receipt_header_html = fields.Html(string="Header", default="", help="Custom HTML header for receipts")
    receipt_footer_html = fields.Html(string="Footer", default="", help="Custom HTML footer for receipts")
