from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    parent_sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        readonly=True,
        ondelete="cascade",
        string="parent sale order line id",
    )

    def action_remove_all_products(self):
        # tmp=[]
        # for i in (self.order_id.order_line):
        #     tmp.append(i.product_template_id.name)
        self.order_id.write({"order_line": [(6, 0, False)]})
