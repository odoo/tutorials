from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # open warranty wizard action
    def action_open_warranty_wizard(self):
        self.ensure_one()
        return self.env['product.warranty'].with_context(default_sale_order_id=self.id)._get_records_action(
            name=self.env._("Choose Warranty"),
            target='new'
        )
