from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product = fields.Many2one(
        string="Deposit Product",
        help="This product will be used to add deposit in the Rental Order.",
        comodel_name="product.product",
        related="company_id.deposit_product",
        readonly=False,
        domain=[("type", "=", "service")],
    )
