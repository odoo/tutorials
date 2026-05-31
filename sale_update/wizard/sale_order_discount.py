from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def action_apply_discount(self):
        self.ensure_one()
        record = self.with_company(self.company_id)
        if record.discount_type == "sol_discount":
            record.sale_order_id.order_line.write(
                {"discount": record.discount_percentage * 100}
            )
        else:
            record.sale_order_id.discount_record_id = record.env[
                "sale.order.discount.record"
            ].create(
                {
                    "discount_id": record.id,
                    "discount_percentage": record.discount_percentage,
                }
            )
            record._create_discount_lines()
