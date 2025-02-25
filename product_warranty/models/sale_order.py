from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_button = fields.Boolean(
        compute="_compute_show_warranty_button", default=False
    )

    def action_add_warranty(self):
        self.ensure_one()
        return {
            "name": "Add Warranty",
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "product.add.warranty",
            "view_mode": "form", 
        }

    @api.depends("order_line.product_id")
    def _compute_show_warranty_button(self):
        for record in self:
            record.show_warranty_button = any(
                line.product_id.is_warranty for line in record.order_line
            )
