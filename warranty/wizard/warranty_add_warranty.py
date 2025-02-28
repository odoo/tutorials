from odoo import fields, models, api, _
import re

class AddWarrantyWizard(models.TransientModel):
    _name = "warranty.add.warranty"
    _description = "Wizard for adding warranty"

    sale_order_id = fields.Many2one(
        'sale.order', default=lambda self: self.env.context.get('default_sale_order_id'), required=True)
    product_ids = fields.Many2many("product.template", store=True, readonly=False)

    product_warranty_ids = fields.One2many("warranty.wizard.lines","wizard_id", readOnly=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super(AddWarrantyWizard, self).default_get(fields_list)

        sale_order_id = self.env.context.get("default_sale_order_id")
        sale_order = self.env["sale.order"].browse(sale_order_id)

        #get available prodcuts from order lines
        available_products = sale_order.order_line.filtered(
            lambda l: not l.related_product_id and l.product_id.product_tmpl_id.warranty and
                      not sale_order.order_line.filtered(lambda w: w.related_product_id == l.product_id.product_tmpl_id)
        ).mapped("product_id.product_tmpl_id")        
        defaults["product_ids"] = [(6, 0, available_products.ids)]

        product_warranty_data = []
        for line in available_products:
            related_line = sale_order.order_line.filtered(lambda l: l.product_id.product_tmpl_id == line)
            quantity = sum(related_line.mapped("product_uom_qty")) if related_line else 1  # Default to 1 if not found - so it does not give error

            product_warranty_data.append((0, 0, {
                'product_id': line.id,
                'year': False,  # Year needs to be selected manually
                'end_date': False,
                'quantity': quantity,
            }))

        if product_warranty_data:
            defaults["product_warranty_ids"] = product_warranty_data
        return defaults


    def action_add_warranty_from_wizard(self):
        self.ensure_one()

        for warranty_line in self.product_warranty_ids:
            print("hellohellohello"+str(warranty_line.quantity))
            if not warranty_line.year:
                continue  # Skip entries where warranty year is not selected

            description = f"[{warranty_line.product_id.name}'s warranty end date is {warranty_line.end_date.strftime('%Y-%m-%d') if warranty_line.end_date else 'N/A'}"
            price = warranty_line.product_id.list_price * warranty_line.year.percentage / 100
            sale_order_line_vals = {
                'order_id': self.sale_order_id.id,
                'product_id': warranty_line.year.product_id.product_variant_id.id,
                'name': description,
                'product_uom_qty': warranty_line.quantity, 
                'price_unit': price,
                'price_subtotal': price * warranty_line.quantity,
                'tax_id': False,
                'related_product_id': warranty_line.product_id.id,
            }
            self.env['sale.order.line'].create(sale_order_line_vals)
            