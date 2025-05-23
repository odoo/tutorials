# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models

class WarrantyWizard(models.TransientModel):
    _name = 'warranty.wizard'

    warranty_line_wizard_ids = fields.One2many(comodel_name='warranty.line.wizard', inverse_name='warranty_wizard_id')

    @api.model
    def default_get(self, fields_list):
        defaults = super(WarrantyWizard, self).default_get(fields_list)
        sale_order_lines = self.env['sale.order'].search([('id', '=', self.env.context.get('active_id'))]).order_line
        warranty_line_wizard_data = []
        for sale_order_line in sale_order_lines:
            if sale_order_line.product_id.product_tmpl_id.is_warranty_available:
                new_warranty_line_data = {
                    'product_id': sale_order_line.product_id,
                    'sale_order_line_id': sale_order_line
                }
                if sale_order_line.child_sale_order_line_id:
                    new_warranty_line_data['warranty_configuration_id'] = sale_order_line.warranty_configuration_id
                warranty_line_wizard_data.append(
                    Command.create(new_warranty_line_data)
                )
        defaults.update({
            'warranty_line_wizard_ids': warranty_line_wizard_data
        })
        return defaults

    def add_warranty(self):
        for warranty_line in self.warranty_line_wizard_ids:
            sale_line = warranty_line.sale_order_line_id
            child_line = sale_line.child_sale_order_line_id
            warranty_config = warranty_line.warranty_configuration_id
            if warranty_config:
                if child_line:
                    child_line.product_id = warranty_config.product_id.id
                    child_line.price_unit = sale_line.price_unit * (warranty_config.percentage / 100)
                    child_line.name = f"{warranty_config.product_id.product_tmpl_id.name}\nEnd Date: {warranty_line.end_date}"
                else:
                    sale_line.child_sale_order_line_id = self.env['sale.order.line'].create({
                            'product_id': warranty_config.product_id.id,
                            'product_uom_qty': sale_line.product_uom_qty,
                            'price_unit': sale_line.price_unit * (warranty_config.percentage/100),
                            'name': f"{warranty_config.product_id.product_tmpl_id.name}\nEnd Date: {warranty_line.end_date}",
                            'order_id': self.env.context.get('active_id'),
                            'sequence': sale_line.sequence
                        })
                sale_line.warranty_configuration_id = warranty_config
            else:
                if child_line:
                    child_line.unlink()
                    sale_line.warranty_configuration_id = False
