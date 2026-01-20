from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.partner'

    book_id = fields.One2many("library.book.rent", "customer_id", required=True)
    is_library_member = fields.Boolean('Library Member?', default=False)
