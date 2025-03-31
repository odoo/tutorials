# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class ProductWarrantyWizard(models.TransientModel):
    _name = 'product.warranty.wizard'
    _description = "Product Warranty Wizard"
    
    warranty_line_ids = fields.One2many(comodel_name='product.warranty.wizard.line', inverse_name='warranty_id')
    
    @api.model
    def default_get(self, fields_list):
        default_fields = super().default_get(fields_list)
        current_sale_order_id = self.env.context.get('active_id', [])
        order_lines = self.env['sale.order'].browse(current_sale_order_id).order_line
        valid_order_lines = order_lines.filtered(
            lambda line: line.product_id.product_tmpl_id.is_warranty_available and not line.linked_line_ids
        )
        link_commands = [
            Command.link(
                self.env['product.warranty.wizard.line'].sudo().create({
                    'product_id': valid_order_line.product_id.id,
                    'linked_line_id': valid_order_line.id,
                }).id
            )
            for valid_order_line in valid_order_lines
        ]
        default_fields['warranty_line_ids'] = link_commands
        return default_fields
    
    def action_add_warranty(self):
        current_sale_order_id = self.env.context.get('active_id', [])
        warranty_lines = self.warranty_line_ids
        if not warranty_lines:
            raise UserError(_("No products with warranty availability were found."))
        if len(warranty_lines) != len(warranty_lines.mapped('warranty_configuration_id')):
            raise UserError(_("Please specify a warranty year for all warranty lines."))
        create_commands = [
            Command.create({
                'order_id': current_sale_order_id,
                'sequence': warranty_line.linked_line_id.sequence,
                'product_id': warranty_line.warranty_configuration_id.product_id.id,
                'price_unit': (
                    warranty_line.warranty_configuration_id.percentage *
                    warranty_line.linked_line_id.price_unit
                )/100,
                'linked_line_id': warranty_line.linked_line_id.id,
            }) 
            for warranty_line in warranty_lines
        ]
        self.env['sale.order'].browse(current_sale_order_id).order_line = create_commands
