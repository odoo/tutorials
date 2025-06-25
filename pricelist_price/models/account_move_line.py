from odoo import api, fields , models


class CustomerInvoice(models.Model):
    _inherit = "account.move.line"

    book_price = fields.Float(string="Book Price", store=True )
    