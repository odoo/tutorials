from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    deposit_amount = fields.Monetary(
        string="Deposit Amount",
        compute="_compute_deposit_amount",
        currency_field="currency_id"
    )
    is_deposit_line = fields.Boolean(
        string="Is Deposit Line",
        help="Indicates whether this line is for a rental deposit",
        default=False
    )

    @api.depends('product_id')
    def _compute_is_deposit_line(self):
        for line in self:
            line.is_deposit_line = line.product_id and line.product_id.is_deposit_product

    def _compute_deposit_amount(self):
        for line in self:
            if line.product_id.rent_ok:
                line.deposit_amount = line.product_id.deposit_amount or (line.price_unit * 0.5)
            else:
                line.deposit_amount = 0.0
