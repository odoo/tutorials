# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_property_id = fields.Many2one("estate.property", string="Property", ondelete="cascade")
