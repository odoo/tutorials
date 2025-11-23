# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    book_price = fields.Float(string="Book Price")
