from odoo import fields, models


class RentalCompany(models.Model):
    _inherit = "res.company"

    deposit_product = fields.Many2one(
        string="Deposit",
        help="This product will be used to add deposits in the Rental Order.",
        comodel_name="product.product",
    )
