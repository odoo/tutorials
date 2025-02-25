from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class WarrantyWizards(models.TransientModel):
    _name = "warranty.wizards"
    _description = "Wizard to Add Warranty to Products"

    order_id = fields.Many2one(
        "sale.order", 
        string="Sale Order", 
        readonly=True
    )
    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        domain="[('order_id', '=', order_id), ('product_id.is_warranty_available', '=', True)]"
    )
    product_id = fields.Many2one(
        "product.product", 
        string="Product", 
        related="order_line_id.product_id", 
        readonly=True
    )
    warranty_id = fields.Many2one(
        "warranty.configuration",
        string="Product Warranty"
    )
    end_date = fields.Date(
        string="End Date", 
        readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))
    
        if sale_order:
            sale_order_lines = sale_order.order_line.filtered(lambda l: l.product_id.is_warranty_available)
    
            if sale_order_lines:
                defaults["order_line_id"] = sale_order_lines[0].id
    
            defaults["order_id"] = sale_order.id
        return defaults
    
    @api.onchange("warranty_id")
    def _onchange_end_date(self):
        for record in self:
            if record.warranty_id:
                end_date = fields.Date.today() + relativedelta(
                    years=int(self.warranty_id.year), 
                    months=int((self.warranty_id.year % 1) * 12)
                )
                record.end_date = end_date

    def apply_warranty(self):
        if not all([self.order_id, self.warranty_id, self.order_line_id]):
            return

        end_date = fields.Date.today() + relativedelta(
            years=int(self.warranty_id.year), 
            months=int((self.warranty_id.year % 1) * 12)
        )

        warranty_vals = {
            "product_id": self.warranty_id.product_template_id.product_variant_id.id,
            "name": f"Warranty: {self.warranty_id.name} for {self.product_id.name} (Valid until: {end_date})",
            "product_uom_qty": 1,
            "price_unit": (self.warranty_id.percentage / 100) * self.product_id.list_price,
        }

        warranty = self.env["sale.order.line"].search([
            ("order_id", "=", self.order_id.id),
            ("linked_order_line_id", "=", self.order_line_id.id),
        ], limit=1)

        if warranty:
            warranty.write(warranty_vals)
        else:
            warranty_vals["order_id"] = self.order_id.id
            warranty_vals["linked_order_line_id"] = self.order_line_id.id
            warranty = self.env["sale.order.line"].create(warranty_vals)

        warranty.sequence = self.order_line_id.sequence + 1
        return {"type": "ir.actions.act_window_close"}
