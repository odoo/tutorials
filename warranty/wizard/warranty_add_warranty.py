from odoo import fields, models, api, _
import re

class AddWarrantyWizard(models.TransientModel):
    _name = "warranty.add.warranty"
    _description = "Wizard for adding warranty"

    sale_order_id = fields.Many2one(
        'sale.order', default=lambda self: self.env.context.get('default_sale_order_id'), required=True)
    product = fields.Many2one(
        "product.template", string="Product",
        domain="[('id', 'in', product_ids)]", required=True)
    year = fields.Many2one("warranty.configuration", string="Year", required=True)
    end_date = fields.Date(compute="_compute_end_date")
    quantity = fields.Float(string="Quantity", readonly=True)
    product_ids = fields.Many2many("product.template", store=True, readonly=False)

    @api.model
    def default_get(self, fields_list):
        defaults = super(AddWarrantyWizard, self).default_get(fields_list)

        sale_order_id = self.env.context.get("default_sale_order_id")
        sale_order = self.env["sale.order"].browse(sale_order_id)

        #get available prodcuts from order lines
        available_products = sale_order.order_line.filtered(lambda l: not l.related_product_id and l.product_id.product_tmpl_id.warranty).mapped("product_id.product_tmpl_id")
        defaults["product_ids"] = [(6, 0, available_products.ids)]

        if available_products:
            defaults["product"] = available_products[0].id # get 1st product as default in wizard

            matching_line = sale_order.order_line.filtered(
                lambda l: l.product_id.product_tmpl_id == available_products[0]
            )
            if matching_line:
                defaults["quantity"] = matching_line[0].product_uom_qty # as well as get its quantity

        return defaults

    # To get updated quantity
    @api.onchange("product")
    def _onchange_product(self):
        if self.product and self.sale_order_id:
            order_line = self.sale_order_id.order_line.filtered(
                lambda l: l.product_id.product_tmpl_id == self.product
            )
            self.quantity = order_line.product_uom_qty if order_line else 0

    def action_add_warranty_from_wizard(self):
        self.ensure_one()

        description = "End Date: " + (self.end_date.strftime('%Y-%m-%d') if self.end_date else "N/A")
        price = self.product.list_price * self.year.percentage / 100
        sale_order_line_vals = {
            'order_id': self.sale_order_id.id,
            'product_id': self.year.product_id.product_variant_id.id,
            'name': description,
            'product_uom_qty': self.quantity,
            'price_unit': price,
            'price_subtotal': price * self.quantity,
            'related_product_id': self.product.id, # for deleting warranty when delete it's product
        }
        
        self.env['sale.order.line'].create(sale_order_line_vals)

    def get_year_number(self):
        match = re.search(r'(\d+)', str(self.year.name))
        return int(match.group(1)) if match else 0

    @api.depends("year.name")
    def _compute_end_date(self):
        for record in self:
            record.end_date = fields.Date.add(fields.Date.today(), years=record.get_year_number())
