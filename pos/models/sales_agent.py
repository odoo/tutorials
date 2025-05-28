from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    sales_agent_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Sales Agent",
        help="Sales agent at the time of billing",
        index=True,
    )

    @api.model
    def _order_fields(self, ui_order):
        """Add sales_agent_id to the order fields."""
        order_fields = super()._order_fields(ui_order)
        if ui_order.get("sales_agent_id"):
            order_fields["sales_agent_id"] = ui_order.get("sales_agent_id")
        return order_fields
