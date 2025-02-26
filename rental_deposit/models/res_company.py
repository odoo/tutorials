from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    extra_deposit = fields.Many2one(
        'product.product',
        domain="[('type', '=', 'service')]")
