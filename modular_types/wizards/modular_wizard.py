from odoo import models, fields


class ModularLineGeneratorWizard(models.TransientModel):
    _name = 'modular.line.generator.wizard'
    _description = 'Wizard to Generate Modular Lines'

    sale_order_id = fields.Many2one('sale.order', string="Sales Order", readonly=True)
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sales Order Line")
    wizard_line_ids = fields.One2many(
        'modular.line.generator.wizard.line',
        'wizard_id',
        string='Modular Lines'
    )

    def action_apply(self):
        self.ensure_one()
        so_line = self.sale_order_line_id or self.env['sale.order.line'].browse(
            self.env.context.get('active_id')
        )
        if not so_line:
            return

        so_line.modular_value_ids.unlink()
        vals_list = []
        for line in self.wizard_line_ids:
            vals_list.append({
                'sale_order_line_id': so_line.id,
                'modular_type_id': line.modular_type_id.id,
                'component_product_id': line.component_product_id.id,
                'quantity': line.new_quantity,
            })
        self.env['sale.order.line.modular.value'].create(vals_list)
        return {'type': 'ir.actions.act_window_close'}

    def action_confirm(self):
        for line in self.wizard_line_ids:
            if line.new_quantity > 0:
                self.env['sale.order.line'].create({
                    'order_id': self.sale_order_id.id,
                    'product_id': line.component_product_id.id,
                    'product_uom_qty': line.new_quantity,
                    'price_unit': 0,
                    'source_modular_type_id': line.modular_type_id.id,
                })
        return {'type': 'ir.actions.act_window_close'}


class ModularLineGeneratorWizardLine(models.TransientModel):
    _name = 'modular.line.generator.wizard.line'
    _description = 'Line for Modular Line Generator Wizard'

    wizard_id = fields.Many2one('modular.line.generator.wizard', required=True, ondelete='cascade')
    modular_type_id = fields.Many2one('modular.type.config', string="Module Type", readonly=True)
    component_product_id = fields.Many2one('product.product', string="Component", readonly=True)
    default_quantity = fields.Float(string="BoM Qty", readonly=True)
    new_quantity = fields.Float(string="Quantity", help="The quantity to add to the Sales Order.")
