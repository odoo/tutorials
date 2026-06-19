from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    library_borrow_id = fields.Many2one('library.borrow')
    member_id = fields.Many2one('library.member')
