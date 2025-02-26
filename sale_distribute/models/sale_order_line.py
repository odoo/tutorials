from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_share_icon = fields.Boolean(
        string="Show Share Icon",
        compute="_compute_show_share_icon",
    )
    shared_amount = fields.Float(string="Shared Amount", default=0.0)
    division_amount_ids = fields.Many2many(
        "sale.order.line.division",
        string="Division",
        help="Shows the amounts added to this line during price distribution.",
    )

    @api.depends('order_id.order_line', 'price_unit')
    def _compute_show_share_icon(self):
        for line in self:
            if len(self.ids) > 1 and line.price_unit > 0:
                line.show_share_icon = True
            else:
                line.show_share_icon = False

    def open_share_wizard(self):
        sale_order = self.order_id
        return {
            "type": "ir.actions.act_window",
            "name": "Distribute Price",
            "view_mode": "form",
            "res_model": "sale.order.line.share.wizard",
            "target": "new",
            "context": {
                "default_sale_order_id": sale_order.id,
                "default_sale_order_line_id": self.id,
            },
        }
