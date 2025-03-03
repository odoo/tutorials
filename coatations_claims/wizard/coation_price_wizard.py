from odoo import api,fields,models

class CoatationPriceWizard(models.TransientModel):
    _name = "coatation.price.wizard"
    _description = "Select negotiated price on the sales order form"
    
  
    coation_lines_ids = fields.Many2many("coatations.lines", string="Coatation Lines")
    order_line_id = fields.Many2one('sale.order.line', string='Order Line')  # Reference to the sale order line
    customer_id = fields.Many2one('res.partner', related="order_line_id.order_id.partner_id", string='Customer', readonly=True)  # Related to the sales order
    coation_ids = fields.Many2one("coatations.claims", string="Coatations Claims")
    domain_ids = fields.Integer()

    @api.model_create_multi
    def default_get(self,fields):
        res = super().default_get(fields)
        print()
        print(self.env.context.get("active_id"))
        active_id=self.env.context.get("active_id")
        # Assuming active_id is the ID of the product (if it's not, you need to adjust this part)
        print(self.env.context)
        product_id= self.env["sale.order.line"].browse(active_id).product_id.id
        sale_order_id = self.env["sale.order.line"].browse(active_id).order_id
        print(sale_order_id.name)
        client_id= sale_order_id.partner_id.id
        if active_id:
            # If the active_id is a product, we assume the context passed active_id as the product ID.
            product = self.env['product.product'].browse(product_id)
            if product:
                print("Product ID:", product.id)
                print(product.name)
                # Query coatations.lines model to get all the coatation_ids for this product_id
                coatation_lines = self.env['coatations.lines'].search([
                    ('product_id', '=', product.id),('coation_id.client_id','=',client_id)
                ])
                
                coatation_ids = coatation_lines.mapped('coation_id.id')
                print("Found Coatation IDs:", coatation_ids)

                print("Name of the ids:",coatation_lines.mapped('coation_id.name'))
                print("Name of the client:",coatation_lines.mapped('coation_id.client_id.name'))
                res.update({"coation_ids": coatation_ids})
        return res

    def action_select_price(self):
        # Method to process the selected price and update the sales order line or take further actions
        # Example: Update the price in the order line based on selected coatation claim/line
        if not self.coation_lines_ids:
            return False  # No price selected

        # Example: Take the first selected coatation line and update the order line's price
        selected_line = self.coation_lines_ids[0]
        selected_price = selected_line.price  # Assuming 'price' is a field in 'coatations.lines'
        self.order_line_id.price_unit = selected_price

        return True
