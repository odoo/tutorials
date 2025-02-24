from odoo import api,fields, models,Command


class SubProductLineWizard(models.TransientModel):
    _name = 'wizard.sub.product.line'
    _description = 'Wizard for Sub Product Line'

    wizard_id = fields.Many2one('wizard.add.sub.products')
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    product_uom_qty = fields.Float()
     
    def create_temp_lines(self):
        sale_order_line_id=self.env.context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        product = sale_order_line.product_id.product_tmpl_id
        sub_product_lines = []
        existing_sub_lines = self.env['wizard.sub.product.line'].search([
            ('wizard_id', '=', self.env.context.get("wizard_id",False))
        ])

        if existing_sub_lines:
            return existing_sub_lines 

        for sub_product in product.sub_product_ids:  
            temp_line = self.create({
                "wizard_id": self.env.context.get("wizard_id", False),
                "product_id": sub_product.id, 
                "price_unit": sub_product.list_price,
                "product_uom_qty": 1,
            })
            sub_product_lines.append(temp_line)

        return sub_product_lines
