from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    property_ids = fields.One2many(
        'estate.property', 'invoice_line_id',
        string='Properties', readonly=True, copy=False)
