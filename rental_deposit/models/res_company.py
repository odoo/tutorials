
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"


    deposit_id = fields.Many2many(
        'product.product', string="Deposit",
        help="The product is used to add the cost to the sales order")
    