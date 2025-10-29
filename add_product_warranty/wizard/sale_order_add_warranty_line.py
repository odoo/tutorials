from datetime import timedelta

from odoo import api, fields, models


class SaleOrderAddWarrantyLine(models.TransientModel):
    _name = "sale.order.add.warranty.line"
    _description = "Line representing a warranty to be added to the sale order"

    wizard_id = fields.Many2one(
        comodel_name="sale.order.add.warranty",
        required=True,
        ondelete="cascade",
    )
    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    warranty_id = fields.Many2one(
        comodel_name="warranty.configuration",
        string="Warranty Configuration",
    )
    end_date = fields.Date(
        string="End Date",
        compute="_compute_end_date",
    )

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_id:
                record.end_date = fields.Date.context_today(record) + timedelta(
                    days=record.warranty_id.period * 365
                )
            else:
                record.end_date = False
