from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
from datetime import timedelta

class ProductWarrantyWizard(models.TransientModel):
    _name = 'product.warranty.wizard'
    _description = 'Warranty Wizard for adding warranties to products in sale orders'

    end_date = fields.Date(string="Warranty End Date", readonly=True, store=True, compute="_calculate_end_date")
    product_ids = fields.Many2one(
        "product.template",
        string="Products",
        domain="[('has_warranty', '=', True)]",
        required=True
    )

    warranty_ids = fields.Many2one("product.warranty", string="Select Warranty", required=True)


    # ------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------

    @api.depends('warranty_ids')
    def _calculate_end_date(self):
        """Calculate the warranty end date based on the selected warranty."""
        if self.warranty_ids.year:
            self.end_date = date.today() + timedelta(days=self.warranty_ids.year * 365)
        else:
            self.end_date = False

    def calculate_warranty_price(self, warranty_percentage, product_price):
        if not warranty_percentage or not product_price:
            return 0.0

        warranty_price = (product_price * warranty_percentage) / 100

        return warranty_price


    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def add_warranty(self):
        """ Adds a warranty with product as a new sale order line. """
        active_order_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_order_id)

        if not sale_order:
            raise ValidationError("No active Sale Order found.")

        if not self.product_ids:
            raise ValidationError("Please select a warranty product.")

        product_price_including_warranty = self.calculate_warranty_price(self.warranty_ids.percentage, self.product_ids.list_price)

        self.product_ids.write({'warranty_id': self.warranty_ids.id})

        self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.warranty_ids.product_id.product_variant_ids.id,
            'name': f"Warranty End Date {self.end_date}",
            'price_unit': product_price_including_warranty,
            'product_uom_qty': 1,
        })
