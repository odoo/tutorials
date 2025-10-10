from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ProductAddWarranty(models.TransientModel):
    _name = "product.add.warranty"
    _description = "Wizard to Add Warranty to Products"

    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        domain="[('order_id', '=', context.get('active_id')), ('product_id.is_warrenty_available', '=', True)]",
    )
    product_id = fields.Many2one(
        "product.product", string="Product", related="order_line_id.product_id", readonly=True
    )
    warranty_id = fields.Many2one("product.warranty", string="Product Warranty", required=True)
    enddate = fields.Date(string="End Date", compute="_compute_enddate", readonly=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        sale_order_id = self.env.context.get("active_id")
        if sale_order_id:
            sale_order = self.env["sale.order"].browse(sale_order_id)
            sale_order_lines = sale_order.order_line.filtered(lambda l: l.product_id.is_warrenty_available)
            if sale_order_lines:
                defaults["order_line_id"] = sale_order_lines[0].id
        return defaults

    @api.depends("warranty_id")
    def _compute_enddate(self):
        """Compute the end date based on the selected warranty period."""
        for record in self:
            if record.warranty_id and record.warranty_id.year:
                record.enddate = datetime.today() + relativedelta(
                    years=int(record.warranty_id.year),
                    months=int((record.warranty_id.year % 1) * 12)
                )
            else:
                record.enddate = False

    def action_confirm(self):
        """Create or update the warranty sale order line using the precomputed end date."""
        sale_order_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(sale_order_id) if sale_order_id else None
        warranty_price = (self.warranty_id.percentage / 100) * self.product_id.list_price
        warranty_product = self.warranty_id.product_template_id.product_variant_id
        warranty_description = f"Warranty for {self.product_id.name} - {self.warranty_id.name} (Ends: {self.enddate})"
        existing_warranty_line = sale_order.order_line.filtered(
            lambda line: line.linked_order_line_id == self.order_line_id
        )

        if existing_warranty_line:
            existing_warranty_line.write({
                "product_id": warranty_product.id,
                "name": warranty_description,
                "price_unit": warranty_price,
            })
        else:
            self.env["sale.order.line"].create({
                "order_id": sale_order.id,
                "product_id": warranty_product.id,
                "name": warranty_description,
                "product_uom_qty": 1,
                "price_unit": warranty_price,
                "linked_order_line_id": self.order_line_id.id,
            })
        return {"type": "ir.actions.act_window_close"}
