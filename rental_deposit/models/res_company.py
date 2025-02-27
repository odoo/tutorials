from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    deposit_product_id = fields.Many2one(
        comodel_name='product.product',
        string="Deposit Product",
        help="This product will be used to add deposits in the Rental Order.",
    )
