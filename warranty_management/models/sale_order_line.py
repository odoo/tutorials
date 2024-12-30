from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_linked = fields.Many2one(
        string="Warranty Linked",
        comodel_name="sale.order.line",
        ondelete="cascade",
        domain="[('order_id', '=', order_id)]",
        copy=False,
        index=True,
    )
    warranty_linked_ids = fields.One2many(
        string="Warranty Link",
        comodel_name="sale.order.line",
        inverse_name="warranty_linked",
    )
