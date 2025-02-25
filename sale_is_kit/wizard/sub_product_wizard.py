from odoo import fields, models, api, Command
from odoo.exceptions import UserError

class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'

    @api.model
    def default_get(self, fields):
        defaults = super(SubProductWizard, self).default_get(fields)
        sale_order_line_id = self.env.context.get('active_id')

        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        product_template = sale_order_line.product_template_id

        existing_wizard = self.env['sub.product.wizard'].search([
            ('sale_order_line_id', '=', sale_order_line_id)
        ], limit=1)

        if existing_wizard:
            defaults.update({
                'sale_order_line_id': sale_order_line_id,
                'line_ids': existing_wizard.line_ids,
            })
        else:
            line_data = []
            for sub_product in product_template.sub_product_ids:
                line_data.append(Command.create({
                    'product_id': sub_product.id,
                    'quantity': 1,
                    'price_unit': sub_product.lst_price,
                }))

            defaults.update({
                'sale_order_line_id': sale_order_line_id,
                'line_ids': line_data,
            })

        return defaults

    
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', required=True, ondelete='cascade')
    line_ids = fields.One2many(comodel_name='sub.product.line', inverse_name='sub_product_wizard_id', string="Sub Products", required=True)

    def action_confirm(self):

        if sum(self.line_ids.mapped('quantity')) == 0:
            raise UserError(_("You must select at least 1 sub-product to purchase the kit product."))
        
        total_price = 0.0
        
        for line in self.line_ids:
            if line.quantity>0:
                self.env['sale.order.line'].create({
                    'order_id': self.sale_order_line_id.order_id.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': 0.0,
                    'parent_line_id': self.sale_order_line_id.id,
                })
            total_price += line.quantity * line.price_unit
        self.sale_order_line_id.price_unit = total_price

        return True

            

        
        
