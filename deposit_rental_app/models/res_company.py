from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    deposit = fields.Many2one("product.product", string="Deposit")
