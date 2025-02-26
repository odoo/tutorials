from odoo import _, Command, api, fields, models
from odoo.exceptions import UserError


class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'

    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', required=True, ondelete="cascade")
    product_id = fields.Many2one(related='sale_order_line_id.product_id', required=True)
    line_ids = fields.One2many(comodel_name='sub.product.line.wizard', inverse_name='sub_product_wizard_id', string="Sub Products", required=True)
    
    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        
        sale_order_line_id = self.env.context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        product = sale_order_line.product_id

        line_data = []
        existing_wizard = self.env['sub.product.wizard'].search([('sale_order_line_id', '=', sale_order_line_id)])

        if existing_wizard:
            for line in existing_wizard.line_ids:
                line_data.append((4, line.id, 0))  # Linking existing records
        else:
            for sub_product in product.sub_product_ids:
                line_data.append((0, 0, {
                    'product_id': sub_product.id,
                    'quantity': 1,
                    'price_unit': sub_product.lst_price,  # Fixed field name
                }))

        defaults.update({
            'sale_order_line_id': sale_order_line_id,
            'line_ids': line_data,  
        })

        return defaults


    def action_confirm(self):
        self.ensure_one()

        # Ensure at least one sub-product is selected
        if not any(self.line_ids.mapped('quantity')):
            raise UserError("You must select at least 1 sub-product to purchase the kit product.")


        sale_order = self.sale_order_line_id.order_id 
        
        existing_sub_lines = {} 
        filtered_lines = self.env['sale.order.line'].search([
            ('parent_line_id', '=', self.sale_order_line_id.id),
            ('order_id', '=', sale_order.id)
        ])

        for line in filtered_lines:
            existing_sub_lines[line.product_id.id] = line 

        total_price = 0.0 

        for wizard_line in self.line_ids:
            sub_product_id = wizard_line.product_id.id

            if sub_product_id in existing_sub_lines:
                # If sub-product exists, update its quantity (price remains 0)
                existing_line = existing_sub_lines[sub_product_id]
                existing_line.write({
                    'product_uom_qty': wizard_line.quantity,
                    'price_unit': 0.0,  
                    'price_subtotal': 0.0, 
                })
            else:
                # If sub-product is new, create a new sale order line
                new_line = self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': sub_product_id,
                    'product_uom_qty': wizard_line.quantity,
                    'price_unit': 0.0,  
                    'price_subtotal': 0.0,  
                    'parent_line_id': self.sale_order_line_id.id,
                })
                existing_sub_lines[sub_product_id] = new_line  

            total_price += wizard_line.quantity * wizard_line.price_unit

        # Update only the main kit product price
        self.sale_order_line_id.update({
            'price_unit': total_price, 
            'price_subtotal': total_price, 
        })

        return True

class SubProductLineWizard(models.TransientModel):
    _name = 'sub.product.line.wizard'
    _sql_constraints = [
        ('check_quantity', "CHECK(quantity >= 0)", "The quantity cannot be negative."),
        ('check_price_unit', "CHECK(price_unit >= 0.0)", "The unit price cannot be negative.")
    ]

    product_id = fields.Many2one(comodel_name='product.product', required=True, ondelete='cascade')
    sub_product_wizard_id = fields.Many2one(comodel_name='sub.product.wizard', required=True, ondelete='cascade')

    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price_unit = fields.Float(string="Unit Price", required=True)
