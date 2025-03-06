from odoo import api, fields, models


class SaleOrderModularTypeWizard(models.TransientModel):
    _name = 'sale.order.modular.type.wizard'
    _description = 'Set Modular Type Values'

    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line",required=True)
    modular_value_ids = fields.One2many(
        comodel_name='sale.order.modular.type.wizard.line',
        inverse_name='wizard_id',
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
                        'value': modular_type.qty_multiplier
                    })
                    for modular_type in sale_order_line.product_id.product_tmpl_id.modular_type_ids
                ],
            })
        return res

    def apply_modular_values(self):
        for wizard in self:
            for modular_value_id in wizard.modular_value_ids:
                self.env['modular.type'].search([('id', '=', modular_value_id.modular_type_id.id)]).write(
                    {'qty_multiplier': modular_value_id.value}
                )
            self.env['sale.order.line'].browse(self.env.context.get('active_id')).write({'is_modular_type_set': True})

class SaleOrderModularTypeWizardLine(models.TransientModel):
    _name = 'sale.order.modular.type.wizard.line'
    _description = 'Wizard Modular Type Value'

    wizard_id = fields.Many2one(comodel_name='sale.order.modular.type.wizard',required=True,ondelete='cascade')
    modular_type_id = fields.Many2one(comodel_name='modular.type',required=True)
    value = fields.Float(default=1.0)
