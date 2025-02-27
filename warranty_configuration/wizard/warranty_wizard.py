from odoo import models, fields, api
from datetime import date, timedelta


class WarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Warranty Wizard"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain=[("is_warranty_available", "=", True)] 
    )
    warranty_year_id = fields.Many2one(
        "warranty.year", string="Warranty Duration", required=True
    )
    warranty_product_id = fields.Many2one(
        "warranty.configuration",
        string="Warranty Configuration",
        compute="_compute_warranty_configuration",
        store=True,
    )
    end_date = fields.Date(
        string="End Date", compute="_compute_end_date", store=True, readonly=True
    )

    @api.depends('warranty_year_id', 'product_id')
    def _compute_warranty_configuration(self):
        for record in self:
            record.warranty_product_id = self.env['warranty.configuration'].search([
                ('warranty_year_id', '=', record.warranty_year_id.id),
            ], limit=1)


    @api.depends("warranty_year_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_year_id:
                record.end_date = date.today() + timedelta(
                    days=record.warranty_year_id.years * 365
                )

 
    def apply_warranty(self):
        active_id = self._context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)
        
        if sale_order and self.warranty_product_id:
            unit_price = (self.product_id.list_price * self.warranty_product_id.percentage) / 100
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': self.warranty_product_id.id,
                'product_warranty_id': self.product_id.id,
                'name': f"{self.warranty_product_id.name}\nEnd Date: {self.end_date}",
                'price_unit': unit_price,
            })
