from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one(
        string="Deposit",
        help="This product will be used to add deposit in the Rental Order.",
        comodel_name="product.product",
        related="company_id.deposit_product_id",
        readonly=False,
    )
