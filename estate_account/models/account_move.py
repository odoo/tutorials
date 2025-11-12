from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    estate_property_id = fields.Many2one("estate.property", string="Estate Property")
