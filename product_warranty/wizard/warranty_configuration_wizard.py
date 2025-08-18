from odoo import fields, models, api
from datetime import timedelta


class WarrantyConfigurationWizard(models.TransientModel):
    _name = "warranty.configuration.wizard"
    _description = "Warranty Configuration Wizard"

    name = fields.Char(string="Name") 
    order_id = fields.Many2one('sale.order')
    order_line_id = fields.Many2one(
        "sale.order.line",
        domain="[('order_id', '=', order_id), ('product_id.is_warranty_available', '=', True)]",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="order_line_id.product_id",
        string="Product",
        readonly=True,
    )
    warranty_id = fields.Many2one(
        comodel_name="warranty.configuration", string="Product Warranty"
    )
    end_date = fields.Date(
        string="End Date", compute="_compute_end_date", readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        order_id = self.env.context.get("default_order_id")
        if order_id:
            sale_order= self.env['sale.order'].browse(order_id)
            sale_order_lines = sale_order.order_line.filtered(
                lambda ln: ln.product_id.is_warranty_available
            )
            if sale_order_lines:
                defaults["order_line_id"] = sale_order_lines[0].id
        return defaults

    @api.depends("warranty_id")
    def _compute_end_date(self):
        for record in self:
            record.end_date = fields.Datetime.today() + timedelta(
                days=record.warranty_id.warranty_period * 365
            )

    def action_add_warranty(self):
        warranty_price = (
            self.warranty_id.percentage / 100
        ) * self.product_id.list_price
        warranty_product = self.warranty_id.product_id
        warranty_description = f"Warranty for {self.product_id.name} - {self.warranty_id.name} (Ends: {self.end_date})"
        existing_warranty_line = self.order_id.order_line.filtered(
            lambda line: line.linked_order_line_id == self.order_line_id
        )
        if existing_warranty_line:
            existing_warranty_line.write(
                {
                    "product_id": warranty_product.product_variant_id.id,
                    "name": warranty_description,
                    "price_unit": warranty_price,
                }
            )
        else:
            self.env["sale.order.line"].create(
                {
                    "order_id": self.order_id.id,
                    "product_id": warranty_product.product_variant_id.id,
                    "name": warranty_description,
                    "product_uom_qty": 1,
                    "price_unit": warranty_price,
                    "linked_order_line_id": self.order_line_id.id,
                }
            )
