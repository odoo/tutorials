from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    sales_rep_id = fields.Many2one(
        "hr.employee",
        string="Sales Representative",
        help="Sales representative at the time of billing",
    )

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super()._order_fields(ui_order)
        if ui_order.get("sales_rep_id"):
            order_fields["sales_rep_id"] = ui_order["sales_rep_id"]
        return order_fields
