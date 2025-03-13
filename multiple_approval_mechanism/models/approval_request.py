from odoo import fields, models
from odoo.exceptions import UserError

class ApprovalRequest(models.Model):
    _inherit = "approval.request"

    sale_order_id = fields.Many2one("sale.order", string="Sales Quotation",  ondelete="cascade")

    def action_open_sale_order(self):
        """Opens the related Sale Quotation."""
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError("No related Sales Quotation found.")

        return {
            "type": "ir.actions.act_window",
            "name": "Sales Quotation",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
            "target": "current",
        }
