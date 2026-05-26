from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    deposit_product = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        help="The product is used to add the deposit to the sales order",
        domain="[('type', '=', 'service')]",
    )
