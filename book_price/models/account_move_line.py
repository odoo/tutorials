# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pricelist_price_unit = fields.Float(string="Book Price", readonly=True)
