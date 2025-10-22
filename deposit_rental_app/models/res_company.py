from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # RENTAL company defaults :

    # Deposit product configured in settings
    deposit_product_id = fields.Many2one(
        "product.product",
        string="Deposit",
        help="This product will be used to add deposit in the Rental Order.",
    )
