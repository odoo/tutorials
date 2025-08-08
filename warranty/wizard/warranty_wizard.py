# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError
class WarrantyWizard(models.TransientModel):
    _name = 'warranty.wizard'
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order", required=True)
    warranty_line_ids = fields.One2many(comodel_name='warranty.line.wizard', inverse_name='wizard_id', string="Warranty Lines")

    @api.model
    def default_get(self,fields_list):
        res = super().default_get(fields_list)
        sale_order_id = self.env.context.get('default_sale_order_id')
        so = self.env['sale.order'].search(domain=[('id','=',sale_order_id)])
        sale_order_line_ids = self.env.context.get('default_sale_order_line_ids')
        if sale_order_id and sale_order_line_ids:
            sale_order_lines = self.env['sale.order.line'].search(domain=[('id','in',sale_order_line_ids)])
            warranty_lines = []
            for line in sale_order_lines:
                new_warranty_line_data = {
                    'product_id': line.product_id,
                    'sale_order_line_id': line,
                }
                warranty_lines.append(
                    Command.create(new_warranty_line_data)
                )
            res.update({
                'sale_order_id': so.id,
                'warranty_line_ids': warranty_lines,
            })
        else:
            raise UserError(_('Add product a with warranty availability to order line.'))
        return res

    def button_add(self):
        so_id = self.env.context.get('default_sale_order_id')
        so = self.env['sale.order'].search(domain=[('id','=',so_id)])
        sol_data=[]
        lines = self.warranty_line_ids.filtered(lambda l: l.warranty_configuration_id)
        for line in lines:
            line.sale_order_line_id.child_sale_order_line_id = self.env['sale.order.line'].create({
                'product_id': line.warranty_configuration_id.product_id.id,
                'product_template_id': line.product_id.product_tmpl_id,
                'product_uom_qty' : 1,
                'order_id' : so_id,
                'name' : line.warranty_configuration_id.product_id.name + '\n' + 'End Date:' + line.end_date.strftime('%m/%d/%Y'),
                'price_unit': (line.product_id.product_tmpl_id.list_price * line.warranty_configuration_id.percentage)/100,
                'sequence': line.sale_order_line_id.sequence,
            })
