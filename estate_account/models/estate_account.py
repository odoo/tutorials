from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    property_id = fields.Many2one("estate.property", string="Property", ondelete="cascade")
