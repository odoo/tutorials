from odoo import api, fields, models


class SaleOrderModularTypeWizard(models.TransientModel):
    _name = 'sale.order.modular.type.wizard'
    _description = 'Set Modular Type Values'

    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', required=True)
    modular_value_ids = fields.One2many(
        comodel_name='sale.order.modular.type.wizard.line',
        inverse_name='modular_type_wizard_id',
        string="Modular Type Values",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        if sale_order_line.product_id.product_tmpl_id:
            res.update({
                'sale_order_line_id': sale_order_line.id,
                'modular_value_ids': [
                    (0, 0, {
                        'modular_type_id': modular_type.id,
                        'modular_quantity': modular_type.qty_multiplier
                    })
                    for modular_type in sale_order_line.product_id.product_tmpl_id.modular_type_ids
                ],
            })
        return res

    def apply_modular_values(self):
        for modular_value_id in self.modular_value_ids:
            modular_value_id.modular_type_id.write({'qty_multiplier': modular_value_id.modular_quantity})
        self.env['sale.order.line'].browse(self.env.context.get('active_id')).write({'is_modular_type_set': True})

class SaleOrderModularTypeWizardLine(models.TransientModel):
    _name = 'sale.order.modular.type.wizard.line'
    _description = 'Wizard Modular Type Value'

    modular_type_wizard_id = fields.Many2one(comodel_name='sale.order.modular.type.wizard', required=True, ondelete='cascade')
    modular_type_id = fields.Many2one(comodel_name='modular.type', required=True, string="Modular Type")
    modular_quantity = fields.Float(default=1.0, string="Quantity")
